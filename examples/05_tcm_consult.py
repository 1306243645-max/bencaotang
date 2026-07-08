"""示例 5: 中医 AI 问诊 — 澳洲用户场景。

运行:
    cd agent-workstation
    .venv/Scripts/python.exe examples/05_tcm_consult.py
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.tcm_agent import create_tcm_agent


def consult(scenario: dict):
    """执行一次问诊。"""
    agent = create_tcm_agent()
    print(f"\n{'─' * 60}")
    print(f"👤 Patient: {scenario['name']}")
    print(f"   Complaint: {scenario['complaint']}")
    print(f"{'─' * 60}")

    resp = agent.chat(scenario["complaint"])
    print(f"🌿 BenCao Tang:\n{resp.content}")
    print(f"\n[Tools used: {len(resp.tool_calls)}]")


def main():
    # ── 场景 1: 失眠 ──
    consult({
        "name": "Sarah, 34F, Melbourne",
        "complaint": (
            "I've been having trouble sleeping for about 3 months now. "
            "I can fall asleep but I wake up at 2-3am every night and can't go back to sleep. "
            "I work a high-stress job, drink 2-3 coffees a day. "
            "My mouth feels dry at night and sometimes I have night sweats. "
            "What's the TCM perspective on this and what can I do naturally?"
        ),
    })

    # ── 场景 2: 消化问题 ──
    consult({
        "name": "Michael, 45M, Sydney",
        "complaint": (
            "I've been feeling bloated and tired after meals for the past few months. "
            "My stool is often loose and I have a hard time concentrating in the afternoon. "
            "I eat a lot of salads and cold foods because it's summer. "
            "I also skip breakfast often and eat a big dinner. "
            "From a TCM view, what's going on and what dietary changes would you suggest?"
        ),
    })

    # ── 场景 3: 药材+穴位咨询 ──
    consult({
        "name": "Emma, 29F, Brisbane",
        "complaint": (
            "I get really bad period pain every month — it's a dull ache in my lower "
            "abdomen that gets worse with cold weather and better with a heat pack. "
            "My flow is dark with some clots, and I feel really tired during my period. "
            "A friend suggested Chinese herbs like Dang Gui and some acupressure. "
            "What TCM pattern does this sound like, what herbs are relevant, "
            "and what acupressure points could I try safely at home?"
        ),
    })


if __name__ == "__main__":
    main()
