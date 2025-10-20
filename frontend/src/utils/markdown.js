import { marked } from 'marked'
import hljs from 'highlight.js'

// 配置marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {
        console.error('代码高亮失败:', err)
      }
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

export function renderMarkdown(text) {
  if (!text) return ''
  return marked(text)
}

export function sanitizeHtml(html) {
  // 简单的HTML清理，防止XSS攻击
  const div = document.createElement('div')
  div.textContent = html
  return div.innerHTML
}
