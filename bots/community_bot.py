"""本草堂 · 微信群运营机器人

功能：自动欢迎语 + 关键词回复 + 每日定时推送 + 积分系统

使用：
    python bots/community_bot.py --mode http --port 9001
    Webhook: http://你的IP:9001/wechat
"""

import sys, json, time, re
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

# ── 配置 ──────────────────────────────────────────────────

CLINIC = {
    "name": "本草堂中医诊所", "phone": "18254191315",
    "wechat": "18254191315", "web": "http://172.20.21.34:8501",
}

# ── 关键词自动回复 ────────────────────────────────────────

KEYWORDS = {
    "体质|自测|测试": lambda: f"🌿 免费体质自测 👉 {CLINIC['web']}\n点击链接，3分钟了解你的中医体质！",
    "预约|挂号|看病": lambda: f"📞 预约电话：{CLINIC['phone']}\n💬 微信：{CLINIC['wechat']}\n或点击链接在线预约 👉 {CLINIC['web']}",
    "地址|位置|在哪": lambda: "📍 山东省济南市历下区经十路123号\n🕐 周一至周五 8:30-17:30，周六 9:00-16:00",
    "失眠|睡不着": lambda: f"😴 失眠调理：\n1. 睡前按神门穴+太冲穴\n2. 菊花枸杞茶替代咖啡\n3. AI 舌诊分析 👉 {CLINIC['web']}",
    "减肥|瘦|胖": lambda: f"⚖️ 中医体质减肥：\n先测体质再减肥！痰湿质和气虚质的减肥方法完全不同\n免费测 👉 {CLINIC['web']}",
    "痛经|月经|姨妈": lambda: f"🌸 痛经分寒凝血瘀和气滞血瘀，你是哪种？\nAI 问诊帮你分析 👉 {CLINIC['web']}",
    "五运六气|运气|出生": lambda: f"🌟 想知道你的出生年运气体质吗？\n输入你的出生年份，我来帮你分析！\n或者去 AI 问诊 👉 {CLINIC['web']}",
    "食谱|食疗|吃什么": lambda: f"🍲 30道中医食疗食谱\n按体质推荐，澳洲食材都能做\n查看 👉 {CLINIC['web']}?page=recipes",
    "产品|商城|买": lambda: f"🛒 养生商城：菊花茶、四神汤、秋梨膏...\n微信下单 👉 {CLINIC['wechat']}",
}

# ── 每日推送内容 ──────────────────────────────────────────

DAILY_TIPS = [
    {"title":"🌿 妙手早安","body":"早上7-9点是胃经当令，一定要吃早餐！一碗热乎乎的小米粥，比什么补品都好。"},
    {"title":"💆 每日一穴","body":"足三里：膝盖下四指，小腿骨外侧。每天按揉5分钟，健脾养胃、增强免疫力。"},
    {"title":"🥗 今日食疗","body":"桂圆红枣茶：桂圆10颗+红枣5颗，沸水焖10分钟。补气血、安神助眠。"},
    {"title":"📖 中医冷知识","body":"为什么中医说'怒伤肝'？长期生气会让肝气郁结，导致失眠、头痛、月经不调。"},
    {"title":"🌟 五运六气","body":"2026丙午年，水运太过+君火司天。今年上半年心火易旺，下半年肺燥明显。养生重点：清心润肺。"},
    {"title":"🍵 下午茶推荐","body":"下午犯困？别喝咖啡！来杯薄荷菊花茶，提神醒脑还不伤胃。"},
    {"title":"🌙 晚安养生","body":"睡前1小时放下手机，泡个脚（40°C，20分钟），按揉涌泉穴100下，今晚睡个好觉。"},
]

# ── 积分系统 ──────────────────────────────────────────────

class PointsSystem:
    def __init__(self, file_path=None):
        self.file = Path(file_path or (Path(__file__).parent.parent / "output" / "points.json"))
        self.file.parent.mkdir(exist_ok=True)
        self.data = self._load()

    def _load(self):
        if self.file.exists():
            return json.loads(self.file.read_text(encoding="utf-8"))
        return {}

    def _save(self):
        self.file.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, user_id, points, reason=""):
        if user_id not in self.data:
            self.data[user_id] = {"points": 0, "history": []}
        self.data[user_id]["points"] += points
        self.data[user_id]["history"].append({
            "points": points, "reason": reason,
            "time": datetime.now().isoformat()
        })
        self._save()
        return self.data[user_id]["points"]

    def get_rank(self, top=10):
        sorted_users = sorted(self.data.items(), key=lambda x: x[1]["points"], reverse=True)
        return sorted_users[:top]

    def get(self, user_id):
        return self.data.get(user_id, {"points": 0, "history": []})


# ── HTTP 服务 ─────────────────────────────────────────────

def run_http(port=9001):
    from flask import Flask, request, jsonify, render_template_string

    app = Flask(__name__)
    pts = PointsSystem()

    # 简易管理后台
    ADMIN_HTML = """<!DOCTYPE html><html><head><title>本草堂·社群管理</title><meta charset="utf-8">
    <style>body{font-family:sans-serif;max-width:800px;margin:2rem auto;padding:1rem}
    .card{background:#f0fdf4;border-radius:1rem;padding:1rem;margin:1rem 0}
    table{width:100%;border-collapse:collapse}th,td{padding:0.5rem;border-bottom:1px solid #ddd}</style></head>
    <body><h1>🌿 本草堂 · 社群管理中心</h1>
    <div class="card"><h3>📊 积分排行榜</h3><table><tr><th>用户</th><th>积分</th></tr>
    {% for uid, info in rank %}<tr><td>{{uid}}</td><td>{{info.points}}</td></tr>{% endfor %}
    </table></div>
    <div class="card"><h3>🔑 关键词回复</h3><ul>{% for kw in keywords %}<li><b>{{kw}}</b></li>{% endfor %}</ul></div>
    <div class="card"><h3>📋 每日推送</h3><ul>{% for tip in tips %}<li>{{tip.title}}: {{tip.body[:50]}}...</li>{% endfor %}</ul></div>
    </body></html>"""

    @app.route("/")
    def admin():
        rank = pts.get_rank(20)
        return render_template_string(ADMIN_HTML, rank=rank,
                                       keywords=list(KEYWORDS.keys()),
                                       tips=DAILY_TIPS)

    @app.route("/wechat", methods=["POST"])
    def wechat():
        data = request.get_json(silent=True) or {}
        msg = data.get("content", data.get("message", "")).strip()
        user = data.get("user", data.get("from", "unknown"))

        reply = ""
        # 关键词匹配
        for pattern, handler in KEYWORDS.items():
            if re.search(pattern, msg, re.IGNORECASE):
                reply = handler()
                break

        if not reply:
            # 出生年份查询（五运六气）
            birth_match = re.search(r"(\d{4})\s*年", msg)
            if birth_match:
                year = int(birth_match.group(1))
                if 1940 <= year <= 2030:
                    reply = f"🔮 根据毛小妹五运六气，{year}年出生的运气体质分析：\n请到 AI 问诊获取详细分析 👉 {CLINIC['web']}\n输入你的出生年份获取专属体质报告！"
                else:
                    reply = f"🌿 感谢咨询！请描述你的症状，或者访问 AI 问诊 👉 {CLINIC['web']}"
            else:
                reply = f"🌿 感谢咨询！我是本草堂智能助手。\n你可以：\n• 输入「体质」开始自测\n• 输入「预约」预约挂号\n• 输入出生年份查运气体质\n• 直接访问 AI 问诊 👉 {CLINIC['web']}"

        # 积分
        pts.add(user, 1, f"咨询: {msg[:30]}")

        return jsonify({"reply": reply})

    @app.route("/push", methods=["POST"])
    def push_daily():
        """每日推送接口"""
        today = datetime.now().day
        tip = DAILY_TIPS[today % len(DAILY_TIPS)]
        return jsonify({"title": tip["title"], "body": tip["body"]})

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "users": len(pts.data)})

    print(f"🌐 社群管理后台: http://localhost:{port}")
    print(f"   Webhook: http://localhost:{port}/wechat")
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="http")
    p.add_argument("--port", type=int, default=9001)
    args = p.parse_args()
    run_http(args.port)
