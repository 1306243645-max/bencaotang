"""示例 3: 实战 — 搜索澳洲经销商 + 生成开发信。

运行:
    cd agent-workstation
    .venv/Scripts/python.exe examples/03_aus_distributor.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.tool_agent import create_tool_agent


def main():
    agent = create_tool_agent(
        system=(
            "你是焊工现代(Hyundai Welder)的海外业务开发经理。\n"
            "焊工现代是中国焊接机器人制造商，正在拓展澳洲市场。\n"
            "规则:\n"
            "1. 用 web_search 搜索，每次搜一个关键词\n"
            "2. 搜索完立刻分析结果、给出结论\n"
            "3. 不要反复搜同一个关键词"
        ),
        max_tokens=8192,
        max_tool_rounds=6,
    )

    print("=" * 60)
    print("焊工现代 — 澳洲经销商搜索")
    print("=" * 60)

    # 第1步：搜索
    resp = agent.chat(
        "搜索 'Australian welding equipment distributors'，列出你找到的公司，"
        "注明公司名、所在地、网站。然后选出最适合做焊工现代焊接机器人经销商的5家，"
        "说明理由。"
    )

    print(f"\n{resp.content}")
    print(f"\n[工具调用: {len(resp.tool_calls)} 次]")

    # 第2步：生成开发信
    if resp.content and "达到最大" not in resp.content:
        resp2 = agent.chat(
            "根据你刚才找到的5家公司，写一封简洁的英文开发信模板。"
            "语气专业亲切，介绍焊工现代的焊接机器人，表达合作意向。"
            "用 [Company Name] 作为公司名占位符。"
        )
        print(f"\n{'=' * 60}")
        print("英文开发信")
        print("=" * 60)
        print(resp2.content)

        # 保存结果
        output_dir = Path(__file__).parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "aus_leads.md"
        output_file.write_text(
            f"# 澳洲经销商开发\n\n"
            f"## 搜索到的公司\n\n{resp.content}\n\n"
            f"## 开发信模板\n\n{resp2.content}\n",
            encoding="utf-8",
        )
        print(f"\n结果已保存: {output_file}")

    print("\n完成。")


if __name__ == "__main__":
    main()
