# cody_tools

Tools for OpenClaw - 为 OpenClaw AI 助手打造的各种实用工具集合。

## 📁 项目结构

```
cody_tools/
├── url_utils/              # URL 工具
│   ├── platform_identifier.py
│   └── README.md
│
├── web_reader/             # 网页内容提取
│   ├── jina_reader.py
│   ├── firecrawl_reader.py
│   ├── playwright_reader.py
│   └── README.md
│
└── smart_url_reader/       # URL 智能读取 SKILL
    ├── smart_reader.py
    ├── obsidian_sync.py
    ├── cli.py
    └── README.md
```

---

## 🌟 核心功能

### 1. URL 智能读取器 (smart_url_reader) ⭐推荐

一键抓取任何网站内容，自动选择最佳策略，并同步到 Obsidian。

**特点：**
- 🤖 智能策略选择（Jina → Firecrawl → Playwright）
- 📋 自动识别 7 大平台
- 📝 一键同步到 Obsidian
- 🖥️ 支持命令行使用

**快速使用：**

```python
from smart_url_reader import smart_read_url, sync_read_result_to_obsidian

# 智能读取
result, error = smart_read_url('https://mp.weixin.qq.com/s/xxxxxx')

# 同步到 Obsidian
sync_read_result_to_obsidian(
    result=result,
    vault_path='/path/to/obsidian/vault',
    folder='Clippings'
)
```

**命令行使用：**

```bash
python -m smart_url_reader.cli "https://zhuanlan.zhihu.com/p/123456" \
    --vault "/Users/name/Documents/Obsidian/Vault"
```

**详细文档：** [smart_url_reader/README.md](smart_url_reader/README.md)

---

### 2. URL 平台识别 (url_utils)

识别 URL 所属的平台及其访问限制。

**支持的平台：**

| 平台 | 域名 | 需要登录 |
|------|------|---------|
| 微信公众号 | mp.weixin.qq.com | 否 |
| 小红书 | xiaohongshu.com, xhslink.com | 否 |
| 知乎 | zhihu.com | 否 |
| 抖音 | douyin.com | 否 |
| 淘宝 | taobao.com, tmall.com | **是** |
| 京东 | jd.com | 否 |
| B站 | bilibili.com, b23.tv | 否 |

**使用示例：**

```python
from url_utils import identify_platform

platform, requires_login = identify_platform('https://mp.weixin.qq.com/s/xxxxxx')
print(f"平台: {platform}, 需要登录: {requires_login}")
# 输出: 平台: 微信公众号, 需要登录: False
```

**详细文档：** [url_utils/README.md](url_utils/README.md)

---

### 3. 网页内容提取 (web_reader)

提供三种策略读取网页内容，供 `smart_url_reader` 调用。

#### 策略一：Jina Reader (推荐)

使用免费服务快速提取网页内容。

```python
from web_reader import read_with_jina

content, error = read_with_jina('https://example.com/article')
```

#### 策略二：Firecrawl (AI 驱动)

AI 驱动的网页抓取，自动处理 JS 渲染和反爬虫。

```python
from web_reader import read_with_firecrawl

os.environ['FIRECRAWL_API_KEY'] = 'your-api-key'
result, error = read_with_firecrawl('https://example.com')
# result: {title, markdown, metadata, url, length}
```

#### 策略三：Playwright (兜底方案)

使用真实浏览器访问，处理需登录页面。

```python
from web_reader import read_with_playwright, save_storage_state

# 保存登录态
save_storage_state(
    url='https://login.taobao.com',
    output_path='./storage/taobao.json',
    headless=False
)

# 使用登录态读取
result, error = read_with_playwright(
    'https://item.taobao.com/item.htm?id=xxx',
    storage_state='./storage/taobao.json'
)
```

#### 策略选择建议

| 场景 | 推荐策略 |
|------|---------|
| 普通网页、新闻文章 | Jina Reader |
| 微信公众号 | Jina Reader |
| 复杂页面、JS 渲染 | Firecrawl |
| 反爬虫严格 | Firecrawl / Playwright |
| 需要登录的页面 | Playwright + 登录态 |

**详细文档：** [web_reader/README.md](web_reader/README.md)

---

## 🚀 安装使用

### 克隆仓库

```bash
git clone git@github.com:coolham/cody_tools.git
cd cody_tools
```

### 安装依赖

```bash
# URL 智能读取器（基础功能，无依赖）

# Firecrawl 支持
pip install firecrawl-py

# Playwright 支持
pip install playwright
playwright install chromium
```

### 环境变量配置

```bash
# Obsidian Vault 路径
export OBSIDIAN_VAULT_PATH="/Users/name/Documents/Obsidian/Vault"

# Firecrawl API Key（可选）
export FIRECRAWL_API_KEY="your-api-key"
```

---

## 📝 开发规范

### 分支管理

- `master`: 主分支，保持稳定
- `feature/xxx`: 功能分支，每个功能独立分支

**工作流程：**

```bash
# 创建新功能分支
git checkout -b feature/new-feature

# 开发完成后提交
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# 在 GitHub 创建 Pull Request 合并到 master
```

### 代码风格

- 使用 Python 3.8+
- 函数添加 docstring 说明
- 类型注解：`from typing import Optional, Tuple, Dict, Any`
- 错误处理：返回 `(result, error)` 元组格式

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 License

GNU General Public License v3.0
