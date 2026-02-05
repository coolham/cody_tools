#!/usr/bin/env python3
"""
URL 智能读取器
整合多种策略智能读取网页内容
"""

import os
import sys
from typing import Optional, Tuple, Dict, Any, Callable
from urllib.parse import urlparse

# 添加上级目录到路径，以便导入其他模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from url_utils import identify_platform
from web_reader import (
    read_with_jina,
    read_with_firecrawl,
    read_with_playwright,
    read_webpage_with_meta as jina_with_meta
)


# 策略优先级配置
STRATEGY_ORDER = ['jina', 'firecrawl', 'playwright']

# 平台默认策略映射
PLATFORM_STRATEGY_MAP = {
    '微信公众号': ['jina', 'firecrawl'],
    '小红书': ['jina', 'firecrawl'],
    '知乎': ['jina', 'firecrawl'],
    '抖音': ['jina', 'firecrawl', 'playwright'],
    '淘宝': ['playwright'],  # 需要登录
    '京东': ['jina', 'firecrawl'],
    'B站': ['jina', 'firecrawl'],
}


def smart_read_url(
    url: str,
    strategies: Optional[list] = None,
    firecrawl_api_key: Optional[str] = None,
    storage_state: Optional[str] = None,
    verbose: bool = False
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    智能读取 URL 内容

    自动选择合适的读取策略，支持多策略回退。

    Args:
        url: 目标网页 URL
        strategies: 指定策略列表 ['jina', 'firecrawl', 'playwright']，默认自动选择
        firecrawl_api_key: Firecrawl API Key，默认从环境变量读取
        storage_state: Playwright 登录态文件路径
        verbose: 是否打印详细日志

    Returns:
        Tuple[结果字典, 错误信息]
        - 成功时返回 ({title, content, source, strategy, ...}, None)
        - 失败时返回 (None, error_message)
    """
    if not url or not isinstance(url, str):
        return None, "URL 不能为空"

    # 识别平台
    platform, requires_login = identify_platform(url)

    if verbose:
        print(f"[SmartReader] 识别平台: {platform or '未知'}, 需要登录: {requires_login}")

    # 确定策略列表
    if strategies is None:
        if platform and platform in PLATFORM_STRATEGY_MAP:
            strategies = PLATFORM_STRATEGY_MAP[platform]
        else:
            strategies = STRATEGY_ORDER.copy()

    # 如果平台需要登录，优先使用 Playwright
    if requires_login and 'playwright' not in strategies:
        strategies = ['playwright'] + strategies

    if verbose:
        print(f"[SmartReader] 使用策略: {strategies}")

    # 按优先级尝试各策略
    last_error = None

    for strategy in strategies:
        if verbose:
            print(f"[SmartReader] 尝试策略: {strategy}")

        result, error = _try_strategy(
            url, strategy,
            firecrawl_api_key=firecrawl_api_key,
            storage_state=storage_state
        )

        if error:
            last_error = f"{strategy}: {error}"
            if verbose:
                print(f"[SmartReader] {strategy} 失败: {error}")
            continue

        # 成功
        result['platform'] = platform
        result['strategy'] = strategy
        result['requires_login'] = requires_login

        if verbose:
            print(f"[SmartReader] {strategy} 成功!")

        return result, None

    # 所有策略都失败
    return None, f"所有策略均失败: {last_error}"


def _try_strategy(
    url: str,
    strategy: str,
    firecrawl_api_key: Optional[str] = None,
    storage_state: Optional[str] = None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """尝试使用指定策略读取 URL"""

    if strategy == 'jina':
        content, error = read_with_jina(url)
        if error:
            return None, error
        return {
            'title': '',  # Jina 不返回标题，需要额外处理
            'content': content,
            'source': url,
            'format': 'markdown'
        }, None

    elif strategy == 'firecrawl':
        if firecrawl_api_key is None:
            firecrawl_api_key = os.environ.get('FIRECRAWL_API_KEY')

        if not firecrawl_api_key:
            return None, "未设置 FIRECRAWL_API_KEY"

        result, error = read_with_firecrawl(url, api_key=firecrawl_api_key)
        if error:
            return None, error

        return {
            'title': result.get('title', ''),
            'content': result.get('markdown', ''),
            'source': url,
            'format': 'markdown',
            'metadata': result.get('metadata', {})
        }, None

    elif strategy == 'playwright':
        result, error = read_with_playwright(url, storage_state=storage_state)
        if error:
            return None, error

        return {
            'title': result.get('title', ''),
            'content': result.get('content', ''),
            'source': url,
            'format': 'text',
            'og_title': result.get('ogTitle', ''),
            'description': result.get('description', '')
        }, None

    else:
        return None, f"未知策略: {strategy}"


def format_for_obsidian(result: Dict[str, Any]) -> str:
    """
    将读取结果格式化为 Obsidian 笔记格式

    Args:
        result: smart_read_url 的返回结果

    Returns:
        Obsidian 格式的 Markdown 字符串
    """
    title = result.get('title', '') or result.get('og_title', '') or '未命名'
    content = result.get('content', '')
    source = result.get('source', '')
    platform = result.get('platform', '未知')
    strategy = result.get('strategy', '未知')
    metadata = result.get('metadata', {})

    # 构建 Obsidian 格式的笔记
    lines = [
        f"# {title}",
        "",
        "> **来源**: " + (f"[{platform}]({source})" if platform != '未知' else f"[{source}]({source})"),
        "> **抓取策略**: {strategy}",
        "",
        "---",
        "",
        content,
        "",
        "---",
        "",
        "## 元数据",
        "",
        f"- **原始 URL**: {source}",
        f"- **平台**: {platform}",
        f"- **抓取策略**: {strategy}",
    ]

    # 添加额外元数据
    if metadata:
        lines.append("")
        lines.append("### 额外信息")
        lines.append("")
        for key, value in metadata.items():
            if value and isinstance(value, (str, int, float)):
                lines.append(f"- **{key}**: {value}")

    return "\n".join(lines)


if __name__ == '__main__':
    # 测试示例
    test_urls = [
        'https://mp.weixin.qq.com/s/xxxxxx',
        'https://zhuanlan.zhihu.com/p/123456',
    ]

    print("URL 智能读取器测试：")
    print("-" * 60)

    for url in test_urls:
        print(f"\n测试 URL: {url}")
        result, error = smart_read_url(url, verbose=True)

        if error:
            print(f"✗ 失败: {error}")
        else:
            print(f"\n✓ 成功!")
            print(f"  平台: {result.get('platform')}")
            print(f"  策略: {result.get('strategy')}")
            print(f"  标题: {result.get('title', 'N/A')[:50]}...")
            print(f"  内容长度: {len(result.get('content', ''))} 字符")

            # 显示 Obsidian 格式预览
            print(f"\n  Obsidian 格式预览:")
            print("  " + "-" * 50)
            obsidian_content = format_for_obsidian(result)
            preview = obsidian_content[:300].replace('\n', '\n  ')
            print(f"  {preview}...")
