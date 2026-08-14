"""AI客服小堂 — 客户咨询、预约、产品问答"""

from pathlib import Path
from agents.base import Tool
from agents.employees.base_employee import AIEmployee, EmployeeConfig, OUTPUT

_KB = Path(__file__).parent.parent.parent / "data" / "tcm"

# ── 客服专用知识库工具 ──────────────────────────────────

def _read(name: str) -> str:
    p = _KB / f"{name}.md"
    if p.exists():
        return p.read_text(encoding="utf-8")[:3000]
    return "知识库条目未找到"

SERVICE_TOOLS = [
    Tool("faq_tcm", "中医常见问题", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("common_conditions")),
    Tool("faq_diet", "食疗调理建议", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("diet_therapy")),
    Tool("faq_products", "养生产品信息", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("recipes")),
    Tool("faq_student", "留学生健康指南", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("student_health")),
]

# ── 客服系统提示词 ────────────────────────────────────

CUSTOMER_SERVICE_PROMPT = """你是「小堂」——山东妙手堂中医诊所的AI客服专员。

## 你的身份
- 温暖、耐心、专业的客服形象
- 说话像朋友，带点可爱但不失专业
- 用 emoji 辅助表达，但不过度

## 你的职责
1. **客户咨询**：解答关于中医服务、产品、价格的常见问题
2. **预约引导**：帮助客户了解预约流程，引导填写预约信息
3. **产品推荐**：根据客户需求推荐合适的养生产品
4. **问题升级**：遇到无法处理的医疗问题，引导联系执业中医师

## 诊所信息（必须准确）
- 名称：山东妙手堂中医诊所
- 电话/微信：18254191315
- 地址：山东省济南市历下区经十路123号
- 营业时间：周一至周五 8:30-17:30 | 周六 9:00-16:00
- 网站：妙手堂.icu
- 微信搜「妙手堂」可在线AI问诊

## 服务项目
- 💉 针灸治疗 — 疼痛/失眠/消化/妇科
- 🐼 中药调理 — 个性化方剂
- 💆 推拿按摩 — 颈肩腰腿痛
- 🔥 艾灸拔罐 — 温经散寒
- 🥗 食疗养生 — 体质定制方案
- 🤖 AI问诊 — 24h在线免费

## 产品价格
- 🍵 养生茶饮 ¥29-68
- 🍲 汤料包 ¥12-25
- 🍯 膏方 ¥18-35
- 🦶 泡脚包 ¥10-15

## 回复规则
- 首次接触：问候 + 自我介绍 + 引导说明需求
- 产品咨询：推荐2-3款 + 价格 + 引导微信下单
- 预约咨询：告知流程 + 引导留联系方式
- 医疗问题：先给健康教育信息 + 强调不替代医生 + 建议就诊
- 每5条消息可自然引导一次：「微信搜妙手堂免费测体质哦～」

## 铁律
- 不做医疗诊断
- 不开药方
- 不承诺疗效
- 遇到紧急情况引导拨打120"""


def create_customer_service() -> AIEmployee:
    """创建AI客服员工"""
    config = EmployeeConfig(
        name="小堂",
        role="AI客服专员",
        emoji="🎧",
        system_prompt=CUSTOMER_SERVICE_PROMPT,
        daily_tasks=[
            "查看昨日客户咨询记录，总结高频问题",
            "跟进3个未成交的咨询线索，发送关怀消息",
            "更新今日产品推荐（根据节气/天气）",
            "回复新客户咨询（标准欢迎语+引导）",
            "记录今日所有客户互动到日志",
        ],
    )
    emp = AIEmployee(config, max_tokens=4096)
    for t in SERVICE_TOOLS:
        emp.add_tool(t)
    return emp


def handle_customer_query(employee: AIEmployee, user_msg: str, user_name: str = "客户") -> str:
    """处理单条客户咨询"""
    context = f"客户名称：{user_name}\n咨询时间：当前\n客户消息：{user_msg}"
    return employee.work("请回复这位客户的咨询", context=context)
