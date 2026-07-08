"""本草堂 · 十大计划自动驾驶系统

自动执行所有可自动化的工作计划，无需人工干预。

每天自动完成:
  计划一: DNS状态检查 + URL更新
  计划二: 全平台内容生成
  计划三: 产品推广文案
  计划四: 课程内容整理
  计划五: 公众号草稿(需AppID)
  计划六: TikTok/海外内容
  计划九: 数据统计报告
  计划十: 知识库自动更新

使用: python bots/auto_worker.py
"""

import sys, json, time, os
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.base import BaseAgent

OUTPUT = Path(__file__).parent.parent / "output"
DAILY = OUTPUT / "daily_report"

class AutoWorker:
    def __init__(self):
        self.agent = BaseAgent(
            system="你是本草堂自动驾驶系统。高效执行所有任务，输出简洁JSON。",
            max_tokens=4096, max_tool_rounds=2
        )
        self.today = datetime.now()
        self.report = {"date": self.today.strftime("%Y-%m-%d"), "tasks": {}}

    def run_all(self):
        """执行所有自动化计划"""
        print(f"\n{'='*55}")
        print(f"  🤖 本草堂自动驾驶 · {self.today.strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*55}\n")

        tasks = [
            ("计划二·每日推广", self.plan_daily_promote),
            ("计划六·海外推广", self.plan_overseas),
            ("计划三·产品带货", self.plan_product_sales),
            ("计划四·课程推广", self.plan_course_promo),
            ("计划九·数据报告", self.plan_data_report),
            ("计划十·自我进化", self.plan_self_evolve),
        ]

    def plan_self_evolve(self):
        """计划十：智能体自我进化"""
        os.system(f'"{sys.executable}" bots/self_evolve.py')
        return "知识库+策略+画像+质量+功能 5项升级完成"

        for name, func in tasks:
            try:
                print(f"[{name}] 执行中...")
                result = func()
                self.report["tasks"][name] = result
                print(f"  ✅ 完成")
            except Exception as e:
                print(f"  ❌ {e}")
                self.report["tasks"][name] = f"失败: {e}"

        self.save_report()

    def plan_daily_promote(self):
        """计划二：每日全平台推广"""
        # 调用现有的 auto_pilot
        os.system(f'"{sys.executable}" bots/auto_pilot.py --mode today')
        return "已生成朋友圈+视频号+小红书文案"

    def plan_overseas(self):
        """计划六：海外TikTok/IG/FB内容"""
        os.system(f'"{sys.executable}" bots/overseas_promote.py --mode content')
        return "已生成TikTok+IG+FB+YT英文内容"

    def plan_product_sales(self):
        """计划三：产品带货话术"""
        os.system(f'"{sys.executable}" bots/overseas_promote.py --mode sales')
        return "已生成今日带货话术"

    def plan_course_promo(self):
        """计划四：知识付费课程推广"""
        courses = ["五运六气入门¥99","金锁玉关风水¥199","人体气象站¥299","周易面诊¥149"]
        prompt = f"为本草堂课程写一句推广语（20字内），推荐课程：{courses[self.today.day%4]}"
        resp = self.agent.chat(prompt)
        path = OUTPUT / "course_promo" / f"promo_{self.today:%Y%m%d}.txt"
        path.parent.mkdir(exist_ok=True)
        path.write_text(resp.content, encoding="utf-8")
        return f"课程推广语: {resp.content[:50]}..."

    def plan_data_report(self):
        """计划九：每日数据报告"""
        stats = {}
        for f in ["bookings.jsonl","orders.jsonl","leads.jsonl"]:
            p = OUTPUT / f
            stats[f.replace(".jsonl","")] = sum(1 for _ in open(p,encoding='utf-8')) if p.exists() else 0
        return stats

    def save_report(self):
        """保存每日工作报告"""
        DAILY.mkdir(parents=True, exist_ok=True)
        path = DAILY / f"report_{self.today:%Y%m%d}.json"
        path.write_text(json.dumps(self.report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📊 工作报告: {path}")
        print(f"   完成 {sum(1 for v in self.report['tasks'].values() if '失败' not in str(v))}/{len(self.report['tasks'])} 项任务")

if __name__ == "__main__":
    worker = AutoWorker()
    worker.run_all()
    print(f"\n🤖 自动驾驶完成。下次运行: 明天早上")
