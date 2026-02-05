# Web Reader 工具

使用 Jina Reader (https://r.jina.ai/) 免费提取网页内容。

## 特点

- 完全免费
- 自动将网页转换为 Markdown 格式
- 支持任意网站（包括需要 JS 渲染的页面）

## 使用方法

```python
from web_reader import read_webpage

# 基本用法
content, error = read_webpage('https://example.com/article')
if error:
    print(f"读取失败: {error}")
else:
    print(content)  # Markdown 格式内容

# 详细信息
from web_reader import read_webpage_with_meta

result = read_webpage_with_meta('https://example.com')
print(result)
# {
#   'success': True,
#   'content': '...markdown content...',
#   'error': None,
#   'url': 'https://example.com',
#   'jina_url': 'https://r.jina.ai/https://example.com'
# }
```

## 原理

Jina Reader 是一个免费服务，只需要在目标 URL 前加上 `https://r.jina.ai/` 即可提取内容。

例如：
- 原 URL: `https://example.com/article`
- Jina URL: `https://r.jina.ai/https://example.com/article`
