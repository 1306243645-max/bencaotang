"""示例 4: 翻译 + 邮件 — 将开发信翻译为中文并模拟发送。

运行:
    cd agent-workstation
    .venv/Scripts/python.exe examples/04_translate_email.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.tool_agent import create_tool_agent


def main():
    agent = create_tool_agent(
        system=(
            "你是焊工现代(Hyundai Welder)的海外业务经理。\n"
            "任务流程：先用 read_file 读取开发信 → 用 translate 翻译 → "
            "用 write_file 保存 → 报告结果。"
            "如需发邮件但未配置，明确告知用户缺少什么配置。"
        ),
    )

    # ── 第1步: 读取 + 翻译 ──
    leads_path = str(Path(__file__).parent.parent / "output" / "aus_leads.md")

    task1 = (
        f"请完成以下任务:\n\n"
        f"1. 用 read_file 读取 {leads_path}\n"
        f"2. 提取其中的英文开发信部分\n"
        f"3. 用 translate 工具将开发信翻译为中文\n"
        f"4. 用 write_file 将中英双语开发信保存到 output/bilingual_email.md\n"
        f"5. 总结你做了什么"
    )

    print("=" * 60)
    print("📝 第1步: 读取 + 翻译开发信")
    print("=" * 60)
    resp = agent.chat(task1)
    print(f"\n{resp.content}")
    print(f"\n[工具调用: {len(resp.tool_calls)} 次]")

    # ── 第2步: 模拟发送 ──
    task2 = (
        "现在用 send_email 工具尝试发送以下邮件:\n\n"
        "收件人: sales@uniautomation.com.au\n"
        "主题: Hyundai Welder - Robotic Welding Solutions | Exploring Partnership\n"
        "正文: (用你刚翻译好的中文版开发信内容)\n\n"
        "如果提示未配置邮件，告诉用户需要去 QQ邮箱/163邮箱 设置里生成授权码，"
        "然后填入 .env 文件。"
    )

    print(f"\n{'=' * 60}")
    print("📧 第2步: 尝试发送邮件")
    print("=" * 60)
    resp2 = agent.chat(task2)
    print(f"\n{resp2.content}")
    print(f"\n[工具调用: {len(resp2.tool_calls)} 次]")

    print(f"\n{'=' * 60}")
    print("完成。查看 output/ 目录下的输出文件。")
    print("=" * 60)


if __name__ == "__main__":
    main()
