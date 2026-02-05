#!/usr/bin/env python3
"""
URL 平台识别工具
用于识别 URL 所属的平台及其访问限制
"""

from urllib.parse import urlparse
from typing import Tuple, Optional


# 平台配置：域名 -> (平台名称, 是否需要登录)
PLATFORM_MAP = {
    # 微信公众号
    'mp.weixin.qq.com': ('微信公众号', False),
    
    # 小红书
    'xiaohongshu.com': ('小红书', False),
    'www.xiaohongshu.com': ('小红书', False),
    'xhslink.com': ('小红书', False),
    
    # 知乎
    'zhihu.com': ('知乎', False),
    'www.zhihu.com': ('知乎', False),
    
    # 抖音
    'douyin.com': ('抖音', False),
    'www.douyin.com': ('抖音', False),
    
    # 淘宝
    'taobao.com': ('淘宝', True),
    'www.taobao.com': ('淘宝', True),
    'item.taobao.com': ('淘宝', True),
    'detail.tmall.com': ('淘宝', True),
    'tmall.com': ('淘宝', True),
    'www.tmall.com': ('淘宝', True),
    
    # 京东
    'jd.com': ('京东', False),
    'www.jd.com': ('京东', False),
    'item.jd.com': ('京东', False),
    
    # B站
    'bilibili.com': ('B站', False),
    'www.bilibili.com': ('B站', False),
    'b23.tv': ('B站', False),
}


def identify_platform(url: str) -> Tuple[Optional[str], bool]:
    """
    识别 URL 所属平台
    
    Args:
        url: 输入的 URL 字符串
        
    Returns:
        Tuple[平台名称, 是否需要登录]
        - 平台名称: 识别到的平台名称，未识别则返回 None
        - 是否需要登录: True/False
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        if not hostname:
            return None, False
        
        # 去除 www. 前缀进行匹配（保留原始匹配作为备选）
        hostname_lower = hostname.lower()
        
        # 直接匹配
        if hostname_lower in PLATFORM_MAP:
            return PLATFORM_MAP[hostname_lower]
        
        # 尝试去除 www. 前缀
        if hostname_lower.startswith('www.'):
            hostname_no_www = hostname_lower[4:]
            if hostname_no_www in PLATFORM_MAP:
                return PLATFORM_MAP[hostname_no_www]
        
        return None, False
        
    except Exception:
        return None, False


def identify_platform_with_info(url: str) -> dict:
    """
    识别 URL 平台并返回详细信息
    
    Args:
        url: 输入的 URL 字符串
        
    Returns:
        dict 包含:
        - platform: 平台名称
        - requires_login: 是否需要登录
        - hostname: 解析后的主机名
        - recognized: 是否成功识别
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        platform, requires_login = identify_platform(url)
        
        return {
            'platform': platform,
            'requires_login': requires_login,
            'hostname': hostname,
            'recognized': platform is not None
        }
    except Exception as e:
        return {
            'platform': None,
            'requires_login': False,
            'hostname': None,
            'recognized': False,
            'error': str(e)
        }


if __name__ == '__main__':
    # 测试示例
    test_urls = [
        'https://mp.weixin.qq.com/s/xxxxxx',
        'https://www.xiaohongshu.com/explore/xxx',
        'https://xhslink.com/xxxx',
        'https://zhihu.com/question/123456',
        'https://www.douyin.com/video/123456',
        'https://item.taobao.com/item.htm?id=123456',
        'https://jd.com/123456.html',
        'https://www.bilibili.com/video/BV1xx411c7mD',
        'https://unknown-site.com/article/123',
    ]
    
    print("URL 平台识别测试结果：")
    print("-" * 60)
    
    for url in test_urls:
        platform, requires_login = identify_platform(url)
        login_status = "需要登录" if requires_login else "无需登录"
        
        if platform:
            print(f"✓ {url[:40]:<40} -> {platform} ({login_status})")
        else:
            print(f"✗ {url[:40]:<40} -> 未识别")
