#!/usr/bin/env python3
"""
Obsidian 同步工具
将内容同步到 Obsidian 仓库
"""

import os
import re
from datetime import datetime
from typing import Optional, Tuple
from urllib.parse import urlparse


def generate_filename(title: str, url: str, max_length: int = 50) -> str:
    """
    根据标题和 URL 生成安全的文件名

    Args:
        title: 文章标题
        url: 原始 URL
        max_length: 文件名最大长度

    Returns:
        安全的文件名（不含扩展名）
    """
    # 清理标题
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_title = safe_title.strip()

    # 如果标题为空，使用 URL 的主机名
    if not safe_title:
        parsed = urlparse(url)
        safe_title = parsed.netloc or 'untitled'

    # 截断过长的标题
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length].strip()

    # 添加日期前缀
    date_prefix = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_prefix} {safe_title}"

    return filename


def sync_to_obsidian(
    content: str,
    vault_path: str,
    folder: str = 'Clippings',
    filename: Optional[str] = None,
    title: str = '',
    url: str = ''
) -> Tuple[bool, Optional[str]]:
    """
    将内容同步到 Obsidian 仓库

    Args:
        content: 要保存的内容（Markdown 格式）
        vault_path: Obsidian Vault 的绝对路径
        folder: 保存的文件夹名称，默认 'Clippings'
        filename: 指定文件名（不含扩展名），默认自动生成
        title: 文章标题，用于生成文件名
        url: 原始 URL，用于生成文件名

    Returns:
        Tuple[是否成功, 错误信息]
    """
    if not content:
        return False, "内容不能为空"

    if not vault_path or not os.path.isdir(vault_path):
        return False, f"Obsidian Vault 路径不存在: {vault_path}"

    # 生成文件名
    if not filename:
        filename = generate_filename(title, url)

    # 确保文件名以 .md 结尾
    if not filename.endswith('.md'):
        filename += '.md'

    # 构建完整路径
    folder_path = os.path.join(vault_path, folder)
    file_path = os.path.join(folder_path, filename)

    # 创建文件夹（如果不存在）
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception as e:
        return False, f"创建文件夹失败: {e}"

    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, None
    except Exception as e:
        return False, f"写入文件失败: {e}"


def sync_read_result_to_obsidian(
    result: dict,
    vault_path: str,
    folder: str = 'Clippings',
    format_func = None
) -> Tuple[bool, Optional[str]]:
    """
    将智能读取的结果同步到 Obsidian

    Args:
        result: smart_read_url 返回的结果字典
        vault_path: Obsidian Vault 路径
        folder: 保存文件夹
        format_func: 格式化函数，默认使用内置格式

    Returns:
        Tuple[是否成功, 错误信息]
    """
    from .smart_reader import format_for_obsidian

    if not result:
        return False, "结果为空"

    # 格式化内容
    if format_func:
        content = format_func(result)
    else:
        content = format_for_obsidian(result)

    # 生成文件名
    title = result.get('title', '') or result.get('og_title', '') or '未命名'
    url = result.get('source', '')

    return sync_to_obsidian(
        content=content,
        vault_path=vault_path,
        folder=folder,
        title=title,
        url=url
    )


if __name__ == '__main__':
    # 测试
    print("Obsidian 同步工具测试：")
    print("-" * 60)

    # 测试文件名生成
    test_cases = [
        ("这是一个很长的标题，需要被截断", "https://example.com/article"),
        ("", "https://zhihu.com/question/123"),
        ("<特殊>字符|测试", "https://test.com"),
    ]

    print("\n文件名生成测试：")
    for title, url in test_cases:
        filename = generate_filename(title, url)
        print(f"  标题: {title[:30] if title else '(空)':<30} -> {filename}.md")
