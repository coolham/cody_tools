# cody_tools

Tools for OpenClaw - 为 OpenClaw AI 助手打造的各种实用工具集合。

## 📁 项目结构

```
cody_tools/
├── url_utils/          # URL 工具
│   ├── platform_identifier.py  # URL 平台识别
│   └── README.md
│
└── web_reader/         # 网页内容提取
    ├── jina_reader.py          # Jina Reader 策略
    ├── firecrawl_reader.py     # Firecrawl AI 策略
    ├── playwright_reader.py    # Playwright 兜底策略
    └── README.md
```

---

## 🔧 功能模块

### 1. URL 平台识别 (url_utils)

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

### 2. 网页内容提取 (web_reader)

提供三种策略读取网页内容，适应不同场景。

#### 2.1 Jina Reader (推荐)

使用免费服务快速提取网页内容。

- ✅ 完全免费
- ✅ 速度快，无需等待
- ✅ 返回 Markdown 格式

```python
from web_reader import read_with_jina

content, error = read_with_jina('https://example.com/article')
```

#### 2.2 Firecrawl (AI 驱动)

AI 驱动的网页抓取，自动处理 JS 渲染和反爬虫。

- ✅ 自动绕过反爬机制
- ✅ 支持复杂页面
- ⚠️ 需要 API Key

```python
from web_reader import read_with_firecrawl
import os

os.environ['FIRECRAWL_API_KEY'] = 'your-api-key'
result, error = read_with_firecrawl('https://example.com')
# result: {title, markdown, metadata, url, length}
```

#### 2.3 Playwright (兜底方案)

使用真实浏览器访问，处理需登录页面。

- ✅ 支持登录态加载
- ✅ 模拟真实浏览器
- ⚠️ 需要安装浏览器

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
# URL 工具（无额外依赖）

# 网页读取 - Jina Reader（urllib，Python 内置）

# 网页读取 - Firecrawl
pip install firecrawl-py

# 网页读取 - Playwright
pip install playwright
playwright install chromium
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
