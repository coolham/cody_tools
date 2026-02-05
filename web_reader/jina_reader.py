#!/usr/bin/env python3
"""
Jina Reader 网页内容提取工具
使用 https://r.jina.ai/ 服务免费提取网页内容
"""

import urllib.request
import urllib.error
from typing import Optional, Tuple


JINA_READER_BASE = "https://r.jina.ai/"


def read_webpage(url: str, timeout: int = 30) -> Tuple[Optional[str], Optional[str]]:
    """
    使用 Jina Reader 读取网页内容
    
    Args:
        url: 目标网页 URL
        timeout: 请求超时时间（秒），默认 30 秒
        
    Returns:
        Tuple[内容, 错误信息]
        - 成功时返回 (markdown_content, None)
        - 失败时返回 (None, error_message)
    """
    if not url or not isinstance(url, str):
        return None, "URL 不能为空"
    
    # 构建 Jina Reader URL
    jina_url = JINA_READER_BASE + url
    
    # 设置请求头
    headers = {
        'Accept': 'text/markdown',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        request = urllib.request.Request(jina_url, headers=headers)
        
        with urllib.request.urlopen(request, timeout=timeout) as response:
            # 检查 HTTP 状态码
            if response.status != 200:
                return None, f"HTTP 错误: {response.status}"
            
            # 读取内容
            content = response.read().decode('utf-8')
            
            # 检查内容是否有效
            if not content or not content.strip():
                return None, "返回内容为空"
            
            # 检查是否返回了错误信息
            if content.startswith('Failed to fetch') or 'Error:' in content[:100]:
                return None, f"Jina Reader 无法提取该页面: {content[:200]}"
            
            return content, None
            
    except urllib.error.HTTPError as e:
        return None, f"HTTP 错误 {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URL 错误: {e.reason}"
    except TimeoutError:
        return None, f"请求超时（{timeout}秒）"
    except Exception as e:
        return None, f"未知错误: {str(e)}"


def read_webpage_with_meta(url: str, timeout: int = 30) -> dict:
    """
    读取网页并返回详细信息
    
    Args:
        url: 目标网页 URL
        timeout: 请求超时时间（秒）
        
    Returns:
        dict 包含:
        - success: 是否成功
        - content: 内容（成功时）
        - error: 错误信息（失败时）
        - url: 原始 URL
        - jina_url: 使用的 Jina Reader URL
    """
    content, error = read_webpage(url, timeout)
    
    return {
        'success': error is None,
        'content': content,
        'error': error,
        'url': url,
        'jina_url': JINA_READER_BASE + url
    }


if __name__ == '__main__':
    # 测试示例
    test_urls = [
        'https://mp.weixin.qq.com/s/xxxxxx',
        'https://zhuanlan.zhihu.com/p/123456',
        'https://www.zhihu.com/question/123456',
    ]
    
    print("Jina Reader 测试：")
    print("-" * 60)
    
    for url in test_urls:
        print(f"\n测试 URL: {url}")
        content, error = read_webpage(url)
        
        if error:
            print(f"✗ 失败: {error}")
        else:
            preview = content[:200].replace('\n', ' ') if content else ""
            print(f"✓ 成功! 内容长度: {len(content)} 字符")
            print(f"  预览: {preview}...")
