# 文件名：llm_orchestrator.py

import requests
import json
import sys


# --- Part 1: Independent Web Search Function ---
def web_search(query: str):
    """
    Calls the bochaAI web search API and returns a formatted string of results.
    This function is self-contained and separate from the LLM call.
    """
    print("【Executing Web Search...】", flush=True)

    url = "https://api.bochaai.com/v1/web-search"
    # 警告：请务必替换为您自己的有效密钥
    headers = {
        'Authorization': 'Bearer sk-b57f9410d9424ede860fc2e408eadba0',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"query": query, "count": 5})

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        if data.get('code') != 200:
            error_msg = f"【Web Search API returned an error: {data.get('msg', 'Unknown error')}】"
            print(error_msg, file=sys.stderr)
            return error_msg

        results_list = data.get('data', {}).get('webPages', {}).get('value', [])
        if not results_list:
            return "【Web search returned no results.】"

        formatted_results = "--- Web Search Results ---\n\n"
        for i, result in enumerate(results_list, 1):
            title = result.get('name', 'No Title')
            content = result.get('summary') or result.get('snippet', 'No content available.')
            content = content.replace('\ue50a', '').replace('\ue50b', '').strip()
            formatted_results += f"[{i}] Title: {title}\n"
            formatted_results += f"    Content: {content}\n\n"

        print("【Web Search Finished】", flush=True)
        return formatted_results.strip()

    except requests.exceptions.RequestException as e:
        error_message = f"【Web Search network request failed: {e}】"
        print(error_message, file=sys.stderr)
        return error_message
    except (json.JSONDecodeError, KeyError) as e:
        error_message = f"【Failed to parse search results JSON: {e}】"
        print(error_message, file=sys.stderr)
        return error_message


# --- Part 2: LLM Call Function with Switches and Additive Prompts ---
def llm_call(
        model: str,
        system_prompt: str,
        user_prompt: str,
        enable_web_search: bool = False,
        enable_deep_thinking: bool = False
):
    """
    Calls the LLM API using a structured system/user prompt approach.
    Can be enhanced with web search (additive prompt) and deep thinking.
    """

    # --- Additive Prompt Construction for User Content ---
    final_user_content = user_prompt

    if enable_web_search:
        # The search query is based on the user's raw prompt
        search_results = web_search(user_prompt)

        # Additive approach: Prepend search results to the user's question
        final_user_content = (
            "Here are the real-time web search results provided for your reference. Please synthesize and answer the user's question based on this information. "
            "If the results are irrelevant, rely on your own knowledge.\n\n"
            f"{search_results}\n\n"
            "--- End of Search Results ---\n\n"
            f"User's Question: {user_prompt}"
        )

    # --- LLM API Payload Construction ---
    url = "https://api.siliconflow.cn/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-xjfkcbhkqyognkrgsgldlgcboubdululbrzzflvnxglofmfg",
        "Content-Type": "application/json"
    }

    # Construct the standard messages list
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_user_content}
    ]

    payload = {
        "model": model,
        "stream": True,
        "messages": messages
    }

    if enable_deep_thinking:
        print("【Deep Thinking Enabled】", flush=True)
        payload["thinking"] = True
    else:
        print("【Standard Mode】", flush=True)

    # --- LLM API Call and Streaming Response ---
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=60)
        response.raise_for_status()

        is_thinking_started = False

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    json_str = decoded_line[6:].strip()
                    if json_str == '[DONE]':
                        break
                    try:
                        data = json.loads(json_str)
                        delta = data.get("choices", [{}])[0].get("delta", {})

                        thinking_content = delta.get("thinking")
                        if enable_deep_thinking and thinking_content:
                            if not is_thinking_started:
                                print("\n--- [Thinking Process] ---\n", end="", flush=True)
                                is_thinking_started = True
                            yield {'type': 'thinking', 'content': thinking_content}

                        answer_content = delta.get("content")
                        if answer_content:
                            yield {'type': 'content', 'content': answer_content}

                    except json.JSONDecodeError:
                        continue

    except requests.exceptions.RequestException as e:
        yield {'type': 'error', 'content': f"\n【LLM API Request Failed: {e}】"}
    except Exception as e:
        yield {'type': 'error', 'content': f"\n【An unexpected error occurred during LLM call: {e}】"}


# --- Main Execution Block ---
if __name__ == '__main__':
    model_id = "zai-org/GLM-4.5-Air"

    # ========== Example 1: Standard Mode (System + User Prompt) ==========
    print("--- Example 1: Standard Mode ---")
    system_1 = "You are a knowledgeable assistant, skilled in explaining complex concepts in a simple and clear manner."
    user_1 = "请解释一下什么是“第一性原理思维”。"
    print(f"System Prompt: {system_1}")
    print(f"User Prompt: {user_1}\n")
    print("Model Response: ", end="")
    for chunk in llm_call(model_id, system_1, user_1):
        if chunk.get('type') == 'content':
            print(chunk['content'], end='', flush=True)
        elif chunk.get('type') == 'error':
            print(chunk['content'], flush=True)
    print("\n" + "=" * 50 + "\n")

    # ========== Example 2: Web Search Mode (System + Additive User Prompt) ==========
    print("--- Example 2: Web Search Mode ---")
    system_2 = "You are a movie and entertainment expert. Your goal is to provide up-to-date and exciting information about upcoming films based on the provided search results."
    user_2 = "2025年有什么值得期待的电影上映？"
    print(f"System Prompt: {system_2}")
    print(f"User Prompt: {user_2}\n")
    # The response will be generated based on the combined prompt
    for chunk in llm_call(model_id, system_2, user_2, enable_web_search=True):
        if chunk.get('type') == 'content':
            print(chunk['content'], end='', flush=True)
        elif chunk.get('type') == 'error':
            print(chunk['content'], flush=True)
    print("\n" + "=" * 50 + "\n")

    # ========== Example 3: Deep Thinking Mode (System + User Prompt) ==========
    print("--- Example 3: Deep Thinking Mode ---")
    system_3 = "You are a meticulous and creative travel planner. Your task is to think step-by-step to design detailed, logical, and enjoyable itineraries based on user requests."
    user_3 = "我计划一次为期5天的北京旅行，请帮我规划一个结合历史与现代的详细行程。"
    print(f"System Prompt: {system_3}")
    print(f"User Prompt: {user_3}\n")

    is_content_started = False
    for chunk in llm_call(model_id, system_3, user_3, enable_deep_thinking=True):
        chunk_type = chunk.get('type')
        chunk_content = chunk.get('content')

        if chunk_type == 'thinking':
            print(chunk_content, end='', flush=True)
        elif chunk_type == 'content':
            if not is_content_started:
                print("\n\n--- [Final Answer] ---\n", end="", flush=True)
                is_content_started = True
            print(chunk_content, end='', flush=True)
        elif chunk_type == 'error':
            print(chunk_content, flush=True)
    print("\n" + "=" * 50 + "\n")