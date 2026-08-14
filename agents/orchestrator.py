"""妙手堂 · AI 员工团队总控中心

每天早上启动，四个 AI 员工各自开工：
  小堂(客服) + 文白(内容) + 千帆(销售) + 墨竹(运营)

用法：
  python agents/orchestrator.py              # 早会模式：全员启动
  python agents/orchestrator.py --mode today # 生成今日全套内容
  python agents/orchestrator.py --mode report # 生成今日运营日报
  python agents/orchestrator.py --mode chat  # 交互模式
"""

import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.employees.customer_service import create_customer_service, handle_customer_query
from agents.employees.content_officer import create_content_officer, generate_daily_content
from agents.employees.sales_assistant import create_sales_assistant, follow_up_lead
from agents.employees.operations import create_operations_manager, daily_report

OUTPUT = Path(__file__).parent.parent / "output" / "employees"


class AIWorkforce:
    """AI 员工团队"""

    def __init__(self):
        self.service = create_customer_service()
        self.content = create_content_officer()
        self.sales = create_sales_assistant()
        self.ops = create_operations_manager()
        self.employees = {
            "小堂": self.service,
            "文白": self.content,
            "千帆": self.sales,
            "墨竹": self.ops,
        }

    def morning_meeting(self):
        """早会：全员报到 + 今日计划"""
        print("=" * 60)
        print("  🌅 妙手堂 · AI 员工早会")
        print(f"  {datetime.now().strftime('%Y年%m月%d日 %A')}")
        print("=" * 60)

        for name, emp in self.employees.items():
            print(f"\n{'━' * 40}")
            print(f"  {emp.config.emoji} {name} — {emp.config.role} 报到")
            print(f"{'━' * 40}")
            try:
                plan = emp.morning_briefing()
                print(f"  📋 今日计划:\n{plan[:500]}")
            except Exception as e:
                print(f"  ⚠️ 启动失败: {e}")

        print(f"\n{'=' * 60}")
        print("  ✅ 早会结束，AI员工团队已就绪")
        print("=" * 60)

    def generate_today_content(self):
        """只用内容官生成今日全套内容"""
        print(f"\n✍️ 文白正在创作今日内容...")
        content = generate_daily_content(self.content)
        print(f"\n{'=' * 60}")
        print(content[:1000])
        print(f"\n{'=' * 60}")
        self._save_output("today_content", content)
        return content

    def generate_daily_report(self):
        """只用运营官生成日报"""
        print(f"\n📊 墨竹正在生成运营日报...")
        report = daily_report(self.ops)
        print(f"\n{'=' * 60}")
        print(report)
        print(f"\n{'=' * 60}")
        self._save_output("daily_report", report)
        return report

    def run_full_day(self):
        """完整的一天工作流"""
        self.morning_meeting()
        print("\n" + "=" * 60)
        print("  📝 内容官创作中...")
        print("=" * 60)
        content = self.generate_today_content()

        print("\n" + "=" * 60)
        print("  📊 运营官生成日报...")
        print("=" * 60)
        report = self.generate_daily_report()

        # 保存日志
        for name, emp in self.employees.items():
            emp.save_log()

        print(f"\n✅ 全天工作完成，日志已保存至 {OUTPUT}")
        return {"content": content, "report": report}

    def _save_output(self, name: str, data: str):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        f = OUTPUT / f"{name}_{datetime.now():%Y%m%d_%H%M}.txt"
        f.write_text(data, encoding="utf-8")
        print(f"📁 已保存: {f}")


def interactive():
    """交互模式 — 与AI员工对话"""
    wf = AIWorkforce()
    print("\n" + "=" * 60)
    print("  🤖 妙手堂 AI 员工团队 · 交互模式")
    print("  输入 'exit' 退出 | 'switch 员工名' 切换员工")
    print("=" * 60)
    print(f"  可用员工: {', '.join(wf.employees.keys())}")
    print(f"  当前员工: 小堂（客服）")

    current = wf.service
    current_name = "小堂"

    while True:
        try:
            msg = input(f"\n🧑 你: ").strip()
            if not msg:
                continue
            if msg.lower() == 'exit':
                break
            if msg.startswith('switch '):
                name = msg[7:].strip()
                if name in wf.employees:
                    current = wf.employees[name]
                    current_name = name
                    print(f"  ✅ 已切换到 {name}")
                else:
                    print(f"  ❌ 未知员工: {name}")
                continue

            print(f"\n{current.config.emoji} {current_name}: ", end="", flush=True)
            resp = current.work(msg)
            print(resp)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n  ⚠️ 错误: {e}")

    print("\n👋 再见！")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="妙手堂 AI 员工团队")
    p.add_argument("--mode", choices=["morning", "today", "report", "full", "chat"], default="morning")
    args = p.parse_args()

    wf = AIWorkforce()

    if args.mode == "chat":
        interactive()
    elif args.mode == "today":
        wf.generate_today_content()
    elif args.mode == "report":
        wf.generate_daily_report()
    elif args.mode == "full":
        wf.run_full_day()
    else:
        wf.morning_meeting()
