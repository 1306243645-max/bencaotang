"""示例 2: 商业助手 — 焊接机器人出口业务。

运行:
    cd agent-workstation
    .venv/Scripts/python.exe examples/02_business_assistant.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.assistant import AssistantAgent


def main():
    print("=" * 50)
    print("焊工现代 — 澳洲业务 AI 助手")
    print("=" * 50)

    assistant = AssistantAgent(
        name="小焊",
        role="焊接机器人出口业务助手，专注于澳洲市场",
        temperature=0.7,
    )

    # 第一轮：了解产品
    q1 = "请用英文写一段100字左右的公司简介，介绍焊工现代(Hyundai Welder)焊接机器人制造商。"
    print(f"\n[User]: {q1}")
    resp = assistant.chat(q1)
    print(f"[Agent]:\n{resp.content}\n")

    # 第二轮：基于上下文继续
    q2 = "Based on that intro, write a 3-sentence email pitch to an Australian distributor."
    print(f"[User]: {q2}")
    resp = assistant.chat(q2)
    print(f"[Agent]:\n{resp.content}\n")

    # 第三轮：市场建议
    q3 = "焊接机器人进入澳洲市场，最重要的三个合规认证是什么？用中英双语回答。"
    print(f"[User]: {q3}")
    resp = assistant.chat(q3)
    print(f"[Agent]:\n{resp.content}\n")

    print(f"\n对话轮次: {len(assistant.history) // 2}")
    print("对话记忆已保留，可以继续追问。")


if __name__ == "__main__":
    main()
