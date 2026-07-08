"""示例 1: 最简 Agent — 验证环境是否正常。

运行:
    cd agent-workstation
    .venv/Scripts/python.exe examples/01_hello_agent.py
"""

import sys
from pathlib import Path

# 修复 Windows GBK 编码问题
sys.stdout.reconfigure(encoding="utf-8")

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings
from agents.base import BaseAgent


def main():
    print("=" * 50)
    print("AI Agent Workstation — Hello World")
    print("=" * 50)
    print(settings.info())
    print("=" * 50)

    agent = BaseAgent(
        system="你是一个友好的助手，用中文回复。",
        temperature=0.7,
    )

    questions = [
        "你好！用一句话介绍一下你自己。",
        "用三个词描述一个好的智能体应该具备什么特质。",
    ]

    for q in questions:
        print(f"\n[User] {q}")
        response = agent.chat(q)
        print(f"[Agent] {response.content}")
        print(f"   [model: {response.model}, tokens: {response.usage}]")


if __name__ == "__main__":
    main()
