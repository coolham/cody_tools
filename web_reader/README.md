# Web Reader 工具

网页内容提取工具集，提供多种策略读取网页内容。

## 策略一：Jina Reader（推荐）

使用 https://r.jina.ai/ 免费服务快速提取网页内容。

### 特点

- 完全免费
- 自动将网页转换为 Markdown 格式
- 速度快，无需等待浏览器启动

### 使用方法

```python
from web_reader import read_with_jina

# 基本用法
content, error = read_with_jina('https://example.com/article')
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

---

## 策略二：Firecrawl（AI 驱动）

使用 Firecrawl API 智能抓取网页，自动处理 JS 渲染和反爬虫。

### 特点

- AI 驱动，自动处理 JavaScript 渲染
- 自动绕过反爬机制
- 直接返回干净的 Markdown
- 支持提取元数据

### 安装依赖

```bash
pip install firecrawl-py
```

### 使用方法

```python
from web_reader import read_with_firecrawl
import os

# 设置 API Key
os.environ['FIRECRAWL_API_KEY'] = 'your-api-key'

# 基本用法
result, error = read_with_firecrawl('https://example.com/article')
if error:
    print(f"读取失败: {error}")
else:
    print(f"标题: {result['title']}")
    print(f"内容: {result['markdown'][:500]}...")
    print(f"元数据: {result['metadata']}")

# 直接传入 API Key
result, error = read_with_firecrawl(
    'https://example.com',
    api_key='your-api-key'
)
```

### 获取 API Key

访问 https://firecrawl.dev 注册并获取 API Key。

---

## 策略三：Playwright（兜底方案）

使用真实浏览器访问页面，处理复杂场景（需要登录、反爬虫等）。

### 特点

- 模拟真实浏览器访问
- 支持加载已保存的登录态
- 使用微信内置浏览器的 User-Agent
- 通过 JS 提取标题和正文

### 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 使用方法

```python
from web_reader import read_with_playwright

# 基本用法（无头模式）
result, error = read_with_playwright('https://example.com')
if error:
    print(f"读取失败: {error}")
else:
    print(f"标题: {result['title']}")
    print(f"内容: {result['content'][:500]}...")

# 带登录态读取
result, error = read_with_playwright(
    'https://example.com/protected',
    storage_state='./storage/taobao.json'
)

# 非无头模式（可见浏览器窗口）
result, error = read_with_playwright(
    'https://example.com',
    headless=False
)
```

### 保存登录态

```python
from web_reader import save_storage_state

# 打开浏览器，手动登录后保存登录态
success, error = save_storage_state(
    url='https://login.taobao.com',
    output_path='./storage/taobao.json',
    headless=False,  # 显示浏览器窗口
    timeout=60       # 等待 60 秒完成登录
)
```

---

## 策略选择建议

| 场景 | 推荐策略 |
|------|---------|
| 普通网页、新闻文章 | Jina Reader |
| 微信公众号 | Jina Reader |
| 复杂页面、JS 渲染 | Firecrawl |
| 反爬虫严格 | Firecrawl / Playwright |
| 需要登录的页面 | Playwright + 登录态 |
| 淘宝等需登录电商 | Playwright + 登录态 |
