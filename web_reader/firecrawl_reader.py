#!/usr/bin/env python3
"""
Firecrawl 网页内容提取工具
使用 Firecrawl AI 驱动的 API 抓取网页
"""

import os
from typing import Optional, Tuple, Dict, Any

# 尝试导入 firecrawl，如果未安装给出友好提示
try:
    from firecrawl import FirecrawlApp
except ImportError:
    FirecrawlApp = None


def read_webpage_firecrawl(
    url: str,
    api_key: Optional[str] = None,
    formats: Optional[list] = None,
    timeout: int = 60
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    使用 Firecrawl 抓取网页内容
    
    Args:
        url: 目标网页 URL
        api_key: Firecrawl API Key，默认从环境变量 FIRECRAWL_API_KEY 读取
        formats: 返回格式列表，默认 ['markdown']
        timeout: 请求超时时间（秒），默认 60 秒
        
    Returns:
        Tuple[结果字典, 错误信息]
        - 成功时返回 ({title, markdown, metadata, url}, None)
        - 失败时返回 (None, error_message)
    """
    if not url or not isinstance(url, str):
        return None, "URL 不能为空"
    
    # 检查 firecrawl 是否已安装
    if FirecrawlApp is None:
        return None, "请先安装 firecrawl: pip install firecrawl-py"
    
    # 获取 API Key
    if api_key is None:
        api_key = os.environ.get('FIRECRAWL_API_KEY')
    
    if not api_key:
        return None, "请设置 FIRECRAWL_API_KEY 环境变量或传入 api_key 参数"
    
    # 设置默认格式
    if formats is None:
        formats = ['markdown']
    
    try:
        # 初始化 Firecrawl
        app = FirecrawlApp(api_key=api_key)
        
        # 调用 scrape 方法
        # Firecrawl v2 返回的是 Document 对象，不是 dict
        result = app.scrape_url(url, params={'formats': formats})
        
        # 处理 Firecrawl v2 的返回值
        # 注意：v2 返回的是对象，不是 dict，需要用 getattr
        markdown = getattr(result, 'markdown', '') or ''
        metadata = getattr(result, 'metadata', {}) or {}
        
        # 从 metadata 获取标题
        title = ''
        if isinstance(metadata, dict):
            title = metadata.get('title', '')
        
        # 如果没有从 metadata 获取到，尝试其他方式
        if not title and hasattr(result, 'title'):
            title = getattr(result, 'title', '')
        
        # 检查内容是否有效
        if not markdown:
            return None, "Firecrawl 返回的内容为空"
        
        # 检查内容长度（过滤掉验证页面、错误页面等）
        if len(markdown) < 100:
            return None, f"内容过短（{len(markdown)} 字符），可能是验证页面或错误页面"
        
        # 检查是否是常见的验证/错误页面
        error_keywords = [
            'captcha', '验证码', '请验证', 'security check',
            'access denied', 'forbidden', 'blocked',
            'please enable javascript', '需要启用 javascript'
        ]
        markdown_lower = markdown.lower()
        for keyword in error_keywords:
            if keyword in markdown_lower:
                return None, f"页面可能包含验证机制: {keyword}"
        
        return {
            'title': title,
            'markdown': markdown,
            'metadata': metadata,
            'url': url,
            'length': len(markdown)
        }, None
        
    except Exception as e:
        return None, f"Firecrawl 错误: {str(e)}"


def read_webpage(
    url: str,
    api_key: Optional[str] = None,
    formats: Optional[list] = None,
    timeout: int = 60
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    同步封装的 Firecrawl 网页读取函数（与 Jina/Playwright 接口保持一致）
    
    参数同 read_webpage_firecrawl()
    """
    return read_webpage_firecrawl(url, api_key, formats, timeout)


if __name__ == '__main__':
    # 测试示例
    test_urls = [
        'https://mp.weixin.qq.com/s/xxxxxx',
        'https://zhuanlan.zhihu.com/p/123456',
        'https://www.zhihu.com/question/123456',
    ]
    
    print("Firecrawl 网页读取测试：")
    print("-" * 60)
    print("注意：需要设置 FIRECRAWL_API_KEY 环境变量")
    print("-" * 60)
    
    # 检查 API Key
    if not os.environ.get('FIRECRAWL_API_KEY'):
        print("\n⚠️ 未设置 FIRECRAWL_API_KEY 环境变量，跳过测试")
        print("获取 API Key: https://firecrawl.dev")
    else:
        for url in test_urls:
            print(f"\n测试 URL: {url}")
            result, error = read_webpage(url)
            
            if error:
                print(f"✗ 失败: {error}")
            else:
                title = result.get('title', 'N/A')
                markdown = result.get('markdown', '')
                preview = markdown[:200].replace('\n', ' ') if markdown else ""
                print(f"✓ 成功!")
                print(f"  标题: {title}")
                print(f"  内容长度: {len(markdown)} 字符")
                print(f"  预览: {preview}...")
