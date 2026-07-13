#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
痛风智能体 Demo 本地预览服务 (serve-preview)
=============================================

用途：
    改 Demo 前/后，起一个本地静态文件服务，把 demos/ 目录暴露成可点击的
    预览 URL，让产品在浏览器里点一遍再拍板，减少"改完才看、理解偏差返工"。

运行：
    python3 design-system/serve-preview.py                 # 默认服务 demos/ 目录，端口 8080
    python3 design-system/serve-preview.py --port 9000     # 自定义端口
    python3 design-system/serve-preview.py --dir demos/医生端  # 只服务某子目录

说明：
    - 纯标准库 http.server，无外部依赖，managed Python 3.13 直接跑。
    - 预览地址示例：http://localhost:8080/患者端/病历夹tab展示页面.html
    - 仅本地访问，不暴露外网；用完 Ctrl+C 关掉即可。

工作流配合（见 design-system/templates/预览说明模板.md）：
    1) 我（小鹿）改 Demo 前，先复制模板填好"改动摘要/受影响屏/受影响红线"；
    2) 起本服务，把预览 URL 连同说明一起发你；
    3) 你在浏览器点验，回复"按此方向改"我才落文件，或"调整 X"我改方向。
"""

import argparse
import http.server
import os
import socketserver
import sys


class _Handler(http.server.SimpleHTTPRequestHandler):
    # 默认服务目录在 __init__ 时由命令行设定（serve_directory）
    def log_message(self, fmt, *args):
        # 精简日志：只打访问路径，不打 User-Agent 等噪声
        sys.stderr.write("  preview ← %s\n" % (args[0] if args else ""))


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)

    parser = argparse.ArgumentParser(description="Demo 本地预览服务")
    parser.add_argument("--port", type=int, default=8080, help="端口（默认 8080）")
    parser.add_argument(
        "--dir",
        default=os.path.join(repo, "demos"),
        help="要服务的目录（默认仓库 demos/）",
    )
    args = parser.parse_args(argv[1:])

    serve_dir = os.path.abspath(args.dir)
    if not os.path.isdir(serve_dir):
        print(f"目录不存在：{serve_dir}")
        return 1

    os.chdir(serve_dir)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", args.port), _Handler) as httpd:
        print("=" * 56)
        print("痛风智能体 Demo 本地预览服务")
        print(f"服务目录: {serve_dir}")
        print(f"预览地址: http://localhost:{args.port}/")
        print("（仅本地访问；Ctrl+C 退出）")
        print("=" * 56)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止预览服务。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
