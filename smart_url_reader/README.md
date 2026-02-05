# URL 智能读取器 (Smart URL Reader)

一键抓取任何网站内容，自动选择最佳策略，并同步到 Obsidian 作为素材库。

## ✨ 功能特点

- 🤖 **智能策略选择** - 自动识别平台并选择最佳读取策略
- 🔄 **多策略回退** - Jina Reader → Firecrawl → Playwright 自动降级
- 📋 **平台识别** - 自动识别微信、知乎、小红书、淘宝等 7 大平台
- 📝 **Obsidian 同步** - 一键保存到 Obsidian Vault，自动格式化
- 🖥️ **命令行工具** - 支持 CLI 快速抓取

---

## 🚀 快速开始

### 安装依赖

```bash
# 基础依赖（Jina Reader）
# 无需额外安装，使用 Python 内置 urllib

# Firecrawl 策略（可选）
pip install firecrawl-py

# Playwright 策略（可选）
pip install playwright
playwright install chromium
```

### 基础用法

```python
from smart_url_reader import smart_read_url, format_for_obsidian

# 智能读取 URL
result, error = smart_read_url('https://mp.weixin.qq.com/s/xxxxxx')

if error:
    print(f"读取失败: {error}")
else:
    # 格式化为 Obsidian 笔记
    note_content = format_for_obsidian(result)
    print(note_content)
```

### 同步到 Obsidian

```python
from smart_url_reader import smart_read_url, sync_read_result_to_obsidian

# 读取 URL
result, error = smart_read_url('https://zhuanlan.zhihu.com/p/123456')

# 同步到 Obsidian
success, error = sync_read_result_to_obsidian(
    result=result,
    vault_path='/path/to/your/obsidian/vault',
    folder='Clippings'  # 保存到 Clippings 文件夹
)
```

---

## 📖 详细用法

### 智能读取

```python
from smart_url_reader import smart_read_url

# 自动选择策略
result, error = smart_read_url('https://example.com/article')

# 指定策略优先级
result, error = smart_read_url(
    url='https://example.com',
    strategies=['firecrawl', 'jina', 'playwright']
)

# 显示详细日志
result, error = smart_read_url(
    url='https://example.com',
    verbose=True
)
```

**返回结果结构：**

```python
{
    'title': '文章标题',
    'content': '文章内容（Markdown）',
    'source': '原始 URL',
    'format': 'markdown',
    'platform': '知乎',  # 识别的平台
    'strategy': 'jina',  # 使用的策略
    'requires_login': False,
    'metadata': {...}  # 额外元数据（Firecrawl）
}
```

### 指定登录态（淘宝等需登录网站）

```python
from smart_url_reader import smart_read_url

result, error = smart_read_url(
    url='https://item.taobao.com/item.htm?id=xxx',
    storage_state='./storage/taobao.json'  # Playwright 登录态
)
```

### 生成 Obsidian 笔记

```python
from smart_url_reader import format_for_obsidian

note = format_for_obsidian(result)
print(note)
```

输出格式：

```markdown
# 文章标题

> **来源**: [知乎](https://zhuanlan.zhihu.com/p/123456)
> **抓取策略**: jina

---

文章内容...

---

## 元数据

- **原始 URL**: https://zhuanlan.zhihu.com/p/123456
- **平台**: 知乎
- **抓取策略**: jina
```

---

## 🖥️ 命令行使用

```bash
# 基础使用
python -m smart_url_reader.cli "https://mp.weixin.qq.com/s/xxxxxx"

# 同步到 Obsidian
python -m smart_url_reader.cli "https://zhuanlan.zhihu.com/p/123456" \
    --vault "/Users/name/Documents/Obsidian/Vault"

# 指定保存文件夹
python -m smart_url_reader.cli "https://example.com" \
    --vault "/path/to/vault" \
    --folder "WebClippings"

# 指定策略
python -m smart_url_reader.cli "https://example.com" \
    --strategy firecrawl jina

# 输出到文件
python -m smart_url_reader.cli "https://example.com" \
    --output "./article.md"

# 显示详细日志
python -m smart_url_reader.cli "https://example.com" --verbose
```

**环境变量：**

```bash
# 设置 Obsidian Vault 路径
export OBSIDIAN_VAULT_PATH="/Users/name/Documents/Obsidian/Vault"

# 设置 Firecrawl API Key
export FIRECRAWL_API_KEY="your-api-key"
```

---

## 🧠 策略说明

### 策略优先级

| 策略 | 速度 | 成本 | 适用场景 |
|------|------|------|---------|
| **Jina Reader** | ⭐⭐⭐ | 免费 | 普通网页、新闻文章、微信公众号 |
| **Firecrawl** | ⭐⭐ | API Key | JS 渲染页面、反爬虫网站 |
| **Playwright** | ⭐ | 免费 | 需登录网站、淘宝等 |

### 平台默认策略

| 平台 | 默认策略 |
|------|---------|
| 微信公众号 | Jina → Firecrawl |
| 知乎 | Jina → Firecrawl |
| 小红书 | Jina → Firecrawl |
| B站 | Jina → Firecrawl |
| 京东 | Jina → Firecrawl |
| 淘宝 | Playwright（需登录）|
| 抖音 | Jina → Firecrawl → Playwright |

---

## 📁 文件结构

```
smart_url_reader/
├── __init__.py           # 包初始化
├── smart_reader.py       # 核心智能读取逻辑
├── obsidian_sync.py      # Obsidian 同步工具
├── cli.py                # 命令行工具
└── README.md             # 本文档
```

---

## ⚙️ 高级配置

### 自定义策略映射

```python
from smart_url_reader import smart_read_url, PLATFORM_STRATEGY_MAP

# 修改某平台的默认策略
PLATFORM_STRATEGY_MAP['知乎'] = ['firecrawl', 'jina']

# 然后调用
result, error = smart_read_url('https://zhihu.com/...')
```

### 自定义 Obsidian 格式

```python
from smart_url_reader.obsidian_sync import sync_read_result_to_obsidian

def my_formatter(result):
    return f"# {result['title']}\n\n{result['content']}"

sync_read_result_to_obsidian(
    result=result,
    vault_path='/path/to/vault',
    format_func=my_formatter
)
```

---

## 🔗 依赖关系

```
smart_url_reader/
    ├── url_utils/          # 平台识别
    │   └── platform_identifier.py
    └── web_reader/         # 读取策略
        ├── jina_reader.py
        ├── firecrawl_reader.py
        └── playwright_reader.py
```

---

## 💡 使用建议

1. **普通网页** - 直接使用，自动选择 Jina Reader
2. **微信公众号** - Jina Reader 效果最佳
3. **知乎/小红书** - 默认策略即可
4. **淘宝/需要登录** - 先用 Playwright 保存登录态
5. **反爬虫网站** - 指定 Firecrawl 或 Playwright
