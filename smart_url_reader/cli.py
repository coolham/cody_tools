#!/usr/bin/env python3
"""
URL 智能读取器 CLI
命令行工具，一键抓取网页并同步到 Obsidian
"""

import os
import sys
import argparse
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from smart_url_reader import smart_read_url, format_for_obsidian
from smart_url_reader.obsidian_sync import sync_read_result_to_obsidian


def main():
    parser = argparse.ArgumentParser(
        description='URL 智能读取器 - 一键抓取网页内容并同步到 Obsidian'
    )

    parser.add_argument('url', help='要抓取的网页 URL')
    parser.add_argument(
        '--vault', '-v',
        default=os.environ.get('OBSIDIAN_VAULT_PATH'),
        help='Obsidian Vault 路径（也可通过 OBSIDIAN_VAULT_PATH 环境变量设置）'
    )
    parser.add_argument(
        '--folder', '-f',
        default='Clippings',
        help='保存到 Obsidian 的文件夹名称（默认: Clippings）'
    )
    parser.add_argument(
        '--strategy', '-s',
        choices=['jina', 'firecrawl', 'playwright'],
        nargs='+',
        help='指定读取策略（默认自动选择）'
    )
    parser.add_argument(
        '--storage-state',
        help='Playwright 登录态文件路径'
    )
    parser.add_argument(
        '--output', '-o',
        help='输出到指定文件（不同步到 Obsidian）'
    )
    parser.add_argument(
        '--verbose', '-V',
        action='store_true',
        help='显示详细日志'
    )

    args = parser.parse_args()

    # 验证 URL
    if not args.url.startswith(('http://', 'https://')):
        print(f"错误: 无效的 URL: {args.url}")
        sys.exit(1)

    # 读取网页
    if args.verbose:
        print(f"开始读取: {args.url}")

    result, error = smart_read_url(
        url=args.url,
        strategies=args.strategy,
        storage_state=args.storage_state,
        verbose=args.verbose
    )

    if error:
        print(f"读取失败: {error}")
        sys.exit(1)

    if args.verbose:
        print(f"\n读取成功!")
        print(f"  平台: {result.get('platform', '未知')}")
        print(f"  策略: {result.get('strategy', '未知')}")
        print(f"  标题: {result.get('title', 'N/A')[:60]}...")
        print(f"  内容长度: {len(result.get('content', ''))} 字符")

    # 输出到文件
    if args.output:
        content = format_for_obsidian(result)
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已保存到: {args.output}")
        except Exception as e:
            print(f"保存文件失败: {e}")
            sys.exit(1)

    # 同步到 Obsidian
    elif args.vault:
        success, error = sync_read_result_to_obsidian(
            result=result,
            vault_path=args.vault,
            folder=args.folder
        )

        if success:
            print(f"已同步到 Obsidian: {args.folder}/")
        else:
            print(f"同步到 Obsidian 失败: {error}")
            sys.exit(1)

    else:
        # 只打印内容
        print("\n" + "=" * 60)
        print(format_for_obsidian(result))
        print("=" * 60)
        print("\n提示: 使用 --vault 参数同步到 Obsidian，或 --output 保存到文件")


if __name__ == '__main__':
    main()
