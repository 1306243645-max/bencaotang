"""妙手堂 · 微信智能体 — 剪贴板模式接入微信"""

import sys, re, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.tcm_agent import create_tcm_agent

agent = create_tcm_agent()
print("[妙手堂] 微信智能体已就绪")


def run_clipboard():
    """剪贴板模式：复制微信消息 -> AI自动回复 -> 粘贴回去

    零封号风险，最安全的方式。
    用法：
        1. 运行此脚本
        2. 微信收到消息 -> Ctrl+C 复制
        3. AI自动分析并生成回复 -> 剪贴板已有回复
        4. 微信对话框 Ctrl+V 粘贴发送
    """
    import pyperclip

    print("=" * 40)
    print("  妙手堂 · 微信智能体 (剪贴板模式)")
    print("=" * 40)
    print()
    print("  使用方法:")
    print("    1. 微信中 Ctrl+C 复制消息")
    print("    2. AI 自动分析生成回复")
    print("    3. 微信中 Ctrl+V 粘贴回复")
    print()
    print("  按 Ctrl+C 退出")
    print("=" * 40)

    last = ""

    while True:
        try:
            current = pyperclip.paste()
            if current != last and len(current.strip()) > 2:
                print(f"\n[收到] {current[:80]}...")
                resp = agent.chat(current)
                reply = resp.content
                pyperclip.copy(reply)
                print(f"[回复] {len(reply)} 字符已复制到剪贴板")
                last = reply
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[退出] 智能体已停止")
            break


if __name__ == "__main__":
    run_clipboard()
