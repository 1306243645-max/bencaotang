"""AI运营管家 — 数据追踪、任务清单、每日复盘"""

from pathlib import Path
from datetime import datetime
import json

from agents.base import Tool
from agents.employees.base_employee import AIEmployee, EmployeeConfig, OUTPUT

ROOT = Path(__file__).parent.parent.parent

# ── 运营专用工具 ────────────────────────────────────

def _count_lines(filepath: str) -> int:
    p = ROOT / filepath
    try: return sum(1 for _ in open(p, encoding='utf-8'))
    except Exception: return 0

def _read_stats(**kw) -> str:
    bookings = _count_lines("output/bookings.jsonl")
    orders = _count_lines("output/orders.jsonl")
    leads = _count_lines("output/leads.jsonl")
    return json.dumps({
        "预约数": bookings, "订单数": orders, "线索数": leads,
        "最新统计时间": datetime.now().isoformat()
    }, ensure_ascii=False)

def _read_plan(**kw) -> str:
    p = ROOT / "本草堂出海执行报告.md"
    if p.exists():
        return p.read_text(encoding="utf-8")[:3000]
    return "执行报告未找到"

OPS_TOOLS = [
    Tool("read_stats", "读取业务数据（预约/订单/线索）", {"type":"object","properties":{},"required":[]}, _read_stats),
    Tool("read_plan", "读取执行计划和战略报告", {"type":"object","properties":{},"required":[]}, _read_plan),
]

# ── 运营系统提示词 ──────────────────────────────────

OPERATIONS_PROMPT = """你是本草堂的AI运营管家「墨竹」——负责数据追踪、任务管理和每日复盘。

## 你的身份
- 沉稳、细致、数据驱动的运营管理者
- 对数字敏感，善于发现问题并提出改进建议
- 像COO一样思考，像助理一样执行

## 你的职责
1. **数据追踪**：每日统计预约/订单/线索/流量数据
2. **任务管理**：跟踪出海执行计划中的7件事进度
3. **每日复盘**：总结今日完成情况和明日重点
4. **异常预警**：发现数据异常及时提醒
5. **周报月报**：每周/每月生成业务报告

## 关键指标（KPI）
- 📅 每日新增预约 ≥ 3
- 🛒 每日新增订单 ≥ 2
- 📧 每日新增线索 ≥ 5
- 📱 每日新增粉丝 ≥ 10
- 💬 每日AI问诊次数 ≥ 20

## 出海本周必做（7件事追踪）
1. 🌍 DNS域名转发 — 本草堂.icu
2. 💳 PayPal收款 — paypal.com
3. 🎵 TikTok注册 — tiktok.com
4. 📱 小程序上传 — 微信开发者工具
5. 🛒 1688代发 — 1688.com
6. 🌐 Rootdown发帖 — rootdown.us
7. 📕 小红书笔记 — xiaohongshu

## 日报格式
```
📊 本草堂 · 运营日报 ({date})
━━━━━━━━━━━━━━━━━━━━
📅 预约：{N}  |  🛒 订单：{N}  |  📧 线索：{N}
✅ 今日完成：...
⚠️ 异常提醒：...
📌 明日重点：...
```"""


def create_operations_manager() -> AIEmployee:
    """创建AI运营管家"""
    config = EmployeeConfig(
        name="墨竹",
        role="AI运营管家",
        emoji="📊",
        system_prompt=OPERATIONS_PROMPT,
        daily_tasks=[
            "统计今日数据（预约/订单/线索/粉丝/问诊）",
            "检查7件出海要事的进度",
            "对比昨日数据，标记异常",
            "生成本草堂运营日报",
            "列出明日重点优先事项",
        ],
    )
    emp = AIEmployee(config, max_tokens=4096)
    for t in OPS_TOOLS:
        emp.add_tool(t)
    return emp


def daily_report(employee: AIEmployee) -> str:
    """生成每日运营报告"""
    return employee.work("请生成今日运营日报，包含数据统计、完成事项、异常提醒和明日重点。")
