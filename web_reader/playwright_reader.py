#!/usr/bin/env python3
"""
Playwright 网页内容提取工具
使用真实浏览器作为兜底方案，处理复杂页面
"""

import asyncio
from typing import Optional, Tuple, Dict, Any
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


# 微信内置浏览器的 User-Agent
WECHAT_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 "
    "MicroMessenger/8.0.38(0x18002628) NetType/WIFI Language/zh_CN"
)


async def read_webpage_playwright(
    url: str,
    storage_state: Optional[str] = None,
    headless: bool = True,
    timeout: int = 30
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    使用 Playwright 读取网页内容
    
    Args:
        url: 目标网页 URL
        storage_state: 已保存的登录态文件路径（JSON 格式）
        headless: 是否使用无头模式，默认 True
        timeout: 页面加载超时时间（秒），默认 30 秒
        
    Returns:
        Tuple[结果字典, 错误信息]
        - 成功时返回 ({title, content, url}, None)
        - 失败时返回 (None, error_message)
    """
    if not url or not isinstance(url, str):
        return None, "URL 不能为空"
    
    browser: Optional[Browser] = None
    context: Optional[BrowserContext] = None
    
    try:
        async with async_playwright() as p:
            # 启动 Chromium 浏览器
            browser = await p.chromium.launch(headless=headless)
            
            # 配置浏览器上下文
            context_options = {
                'user_agent': WECHAT_USER_AGENT,
            }
            
            # 如果提供了 storage_state，加载登录态
            if storage_state:
                context_options['storage_state'] = storage_state
            
            context = await browser.new_context(**context_options)
            
            # 创建新页面
            page = await context.new_page()
            
            # 设置默认超时
            page.set_default_timeout(timeout * 1000)
            
            # 访问目标页面
            await page.goto(url, wait_until='networkidle')
            
            # 使用 JS 提取标题和正文
            result = await page.evaluate("""() => {
                // 提取标题
                const title = document.title || '';
                
                // 尝试提取正文内容
                // 策略：优先查找文章主体区域
                const articleSelectors = [
                    'article',
                    '[role="main"]',
                    '.post-content',
                    '.article-content',
                    '.entry-content',
                    '.content',
                    '#content',
                    '.rich_media_content',  // 微信公众号
                    '.Post-RichTextContainer',  // 知乎
                    '.note-content',  // 小红书
                ];
                
                let content = '';
                
                for (const selector of articleSelectors) {
                    const element = document.querySelector(selector);
                    if (element) {
                        content = element.innerText;
                        break;
                    }
                }
                
                // 如果没找到，提取 body 文本
                if (!content) {
                    const body = document.body;
                    if (body) {
                        // 过滤脚本和样式标签
                        const scripts = body.querySelectorAll('script, style, nav, header, footer, aside');
                        scripts.forEach(el => el.remove());
                        content = body.innerText;
                    }
                }
                
                // 提取元数据
                const description = document.querySelector('meta[name="description"]')?.content || '';
                const ogTitle = document.querySelector('meta[property="og:title"]')?.content || '';
                const ogDescription = document.querySelector('meta[property="og:description"]')?.content || '';
                
                return {
                    title: title,
                    ogTitle: ogTitle,
                    description: description,
                    ogDescription: ogDescription,
                    content: content.trim(),
                    url: window.location.href
                };
            }""")
            
            await context.close()
            await browser.close()
            
            # 检查结果
            if not result or not result.get('content'):
                return None, "无法提取页面内容"
            
            return result, None
            
    except Exception as e:
        # 清理资源
        if context:
            try:
                await context.close()
            except:
                pass
        if browser:
            try:
                await browser.close()
            except:
                pass
        return None, f"Playwright 错误: {str(e)}"


def read_webpage(
    url: str,
    storage_state: Optional[str] = None,
    headless: bool = True,
    timeout: int = 30
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    同步封装的 Playwright 网页读取函数
    
    参数同 read_webpage_playwright()
    """
    return asyncio.run(read_webpage_playwright(url, storage_state, headless, timeout))


async def save_storage_state(
    url: str,
    output_path: str,
    headless: bool = False,
    timeout: int = 60
) -> Tuple[bool, Optional[str]]:
    """
    保存浏览器登录态
    
    Args:
        url: 登录页面 URL
        output_path: 保存路径（JSON 文件）
        headless: 是否无头模式（建议 False，方便手动登录）
        timeout: 等待时间（秒）
        
    Returns:
        Tuple[是否成功, 错误信息]
    """
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(user_agent=WECHAT_USER_AGENT)
            page = await context.new_page()
            
            # 访问页面，等待手动登录
            await page.goto(url)
            
            print(f"请在打开的浏览器中完成登录，等待 {timeout} 秒...")
            await asyncio.sleep(timeout)
            
            # 保存登录态
            await context.storage_state(path=output_path)
            
            await context.close()
            await browser.close()
            
            return True, None
            
    except Exception as e:
        return False, f"保存登录态失败: {str(e)}"


if __name__ == '__main__':
    # 测试示例
    test_urls = [
        'https://mp.weixin.qq.com/s/xxxxxx',
        'https://zhuanlan.zhihu.com/p/123456',
    ]
    
    print("Playwright 网页读取测试：")
    print("-" * 60)
    
    for url in test_urls:
        print(f"\n测试 URL: {url}")
        result, error = read_webpage(url, headless=True)
        
        if error:
            print(f"✗ 失败: {error}")
        else:
            title = result.get('title', 'N/A')
            content = result.get('content', '')
            preview = content[:200].replace('\n', ' ') if content else ""
            print(f"✓ 成功!")
            print(f"  标题: {title}")
            print(f"  内容长度: {len(content)} 字符")
            print(f"  预览: {preview}...")
