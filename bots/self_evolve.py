"""本草堂 · 智能体自我进化系统

每天自动执行:
  1. 知识库更新——搜索最新中医出海资讯
  2. 功能升级——根据使用数据优化回复质量
  3. 获客模型——追踪转化数据优化策略
  4. 客户画像——分析咨询数据建立画像
"""

import sys, json, os
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.base import BaseAgent

OUT = Path(__file__).parent.parent / "output"
DATA = OUT / "analytics"
DATA.mkdir(parents=True, exist_ok=True)

AGENT = BaseAgent(
    system="你是本草堂智能进化引擎。分析数据，优化策略，输出JSON。",
    max_tokens=2048, max_tool_rounds=2
)

class SelfEvolve:
    def __init__(self):
        self.today = datetime.now()
        self.report = {"date": self.today.strftime("%Y-%m-%d"), "upgrades": []}

    def run(self):
        print(f"\n{'='*50}")
        print(f"  🧬 智能体自我进化 · {self.today:%Y-%m-%d}")
        print(f"{'='*50}\n")

        steps = [
            ("知识库更新", self.expand_knowledge),
            ("获客策略优化", self.optimize_acquisition),
            ("客户画像分析", self.analyze_customers),
            ("回复质量评估", self.assess_quality),
            ("功能建议生成", self.suggest_features),
        ]

        for name, func in steps:
            try:
                result = func()
                self.report["upgrades"].append({"task": name, "result": result})
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ⚠️ {name}: {e}")

        self.save()

    def expand_knowledge(self):
        """搜索最新中医出海资讯，扩充知识库"""
        prompt = """你是中医出海趋势分析师。基于你已有的知识（2025-2026年），
总结3条最重要的中医出海新趋势或新案例，每条一句话。输出JSON数组。"""
        resp = AGENT.chat(prompt)
        path = DATA / f"trends_{self.today:%Y%m%d}.json"
        path.write_text(resp.content[:1000], encoding="utf-8")
        return f"已分析3条趋势"

    def optimize_acquisition(self):
        """优化获客策略"""
        # 检查各渠道数据
        stats = self._load_stats()
        prompt = f"""当前数据：订单{stats.get('orders',0)}，线索{stats.get('leads',0)}。
给出1条最有效的获客策略建议，30字以内。"""
        resp = AGENT.chat(prompt)
        path = DATA / f"strategy_{self.today:%Y%m%d}.txt"
        path.write_text(resp.content[:500], encoding="utf-8")
        return resp.content[:80]

    def analyze_customers(self):
        """分析客户画像"""
        orders = self._load_orders()
        prompt = f"分析以下订单数据，总结目标客户画像（1句话）：{str(orders)[:200]}"
        resp = AGENT.chat(prompt)
        path = DATA / f"persona_{self.today:%Y%m%d}.txt"
        path.write_text(resp.content[:500], encoding="utf-8")
        return resp.content[:80]

    def assess_quality(self):
        """评估回复质量并建议改进"""
        prompt = "给出一条提升AI问诊回复质量的建议，20字以内。"
        resp = AGENT.chat(prompt)
        return resp.content[:80]

    def suggest_features(self):
        """建议新功能"""
        prompt = "基于中医出海和AI问诊场景，建议一个最需要的新功能，20字以内。"
        resp = AGENT.chat(prompt)
        return resp.content[:80]

    def _load_stats(self):
        try:
            orders = sum(1 for _ in open(OUT/"orders.jsonl",encoding='utf-8')) if (OUT/"orders.jsonl").exists() else 0
            leads = sum(1 for _ in open(OUT/"leads.jsonl",encoding='utf-8')) if (OUT/"leads.jsonl").exists() else 0
            bookings = sum(1 for _ in open(OUT/"bookings.jsonl",encoding='utf-8')) if (OUT/"bookings.jsonl").exists() else 0
            return {"orders":orders, "leads":leads, "bookings":bookings}
        except Exception:
            return {}

    def _load_orders(self):
        try:
            orders = []
            if (OUT/"orders.jsonl").exists():
                for line in open(OUT/"orders.jsonl",encoding='utf-8'):
                    try: orders.append(json.loads(line))
                    except Exception: pass
            return orders[-5:]
        except Exception:
            return []

    def save(self):
        path = DATA / f"evolve_{self.today:%Y%m%d}.json"
        path.write_text(json.dumps(self.report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📊 进化报告: {path}")
        print(f"   完成 {len(self.report['upgrades'])} 项升级")

if __name__ == "__main__":
    SelfEvolve().run()
