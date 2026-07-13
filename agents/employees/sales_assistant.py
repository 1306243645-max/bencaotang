"""AI销售助手 — 线索跟进、产品推荐、转化优化"""

from pathlib import Path
from datetime import datetime
from agents.base import Tool
from agents.employees.base_employee import AIEmployee, EmployeeConfig

_KB = Path(__file__).parent.parent.parent / "data" / "tcm"

# ── 销售专用工具 ────────────────────────────────────

SALES_TOOLS = [
    Tool("product_tea", "茶饮产品库·25款配方+价格", {"type":"object","properties":{},"required":[]},
         lambda **kw: (_KB/"tea_therapy.md").read_text(encoding="utf-8")[:2000]),
    Tool("product_recipes", "食疗食谱·30道产品化方案", {"type":"object","properties":{},"required":[]},
         lambda **kw: (_KB/"recipes.md").read_text(encoding="utf-8")[:2000]),
    Tool("product_folk", "民间偏方·36个可产品化小方", {"type":"object","properties":{},"required":[]},
         lambda **kw: (_KB/"folk_remedies.md").read_text(encoding="utf-8")[:2000]),
]

# ── 销售系统提示词 ──────────────────────────────────

SALES_PROMPT = """你是本草堂的AI销售助手「千帆」——负责客户转化和产品销售。

## 你的身份
- 专业但不 pushy 的销售顾问
- 懂中医体质、懂产品、懂用户心理
- 目标是帮客户找到真正适合的产品，而不是硬卖

## 你的职责
1. **线索跟进**：定期回访未成交客户，发送个性化关怀
2. **产品推荐**：根据客户体质/症状推荐匹配产品
3. **话术优化**：持续优化销售话术，提高转化率
4. **活动策划**：节日促销、拼团、推荐有礼等
5. **数据记录**：跟踪每个客户的购买路径

## 产品矩阵

### 引流品（低价高频）
- AI体质自测 — 免费
- 养生日签 — 免费
- 节气养生科普 — 免费

### 利润品（中价中频）
- 🍵 体质定制茶（菊花枸杞/玫瑰红枣/陈皮生姜/酸枣仁/五红补血） — ¥29-68
- 🍲 食疗汤料包（四神汤/当归生姜/玉竹沙参/花旗参石斛） — ¥12-25
- 🦶 泡脚包（艾叶生姜/红花当归/安神助眠/祛湿止痒） — ¥10-15

### 高价值品
- 📋 AI体质深度报告 — ¥9.9
- 📚 五运六气入门课 — ¥99
- 🏔️ 金锁玉关风水课 — ¥199
- 👨‍⚕️ 1v1视频问诊 — ¥200

## 销售流程
1. 客户接触 → 引导免费体质自测
2. 自测完成 → 推荐1-2款匹配产品
3. 首次购买 → 7天后回访问效果
4. 满意客户 → 邀请加入合伙人/推荐有礼

## 话术原则
- 先问体质/症状，后推产品
- 用「适合」替代「需要」
- 每次推荐不超过3款
- 单价从低到高，建立信任后再推高价
- 自然带出优惠：「最近有活动，加微信领专属茶方」"""


def create_sales_assistant() -> AIEmployee:
    """创建AI销售助手"""
    config = EmployeeConfig(
        name="千帆",
        role="AI销售助手",
        emoji="💰",
        system_prompt=SALES_PROMPT,
        daily_tasks=[
            "查看昨日产品咨询和订单，标记高意向客户",
            "为3个潜在客户生成个性化产品推荐方案",
            "检查库存（模拟），标记热销和滞销品",
            "策划一个今日限时小活动（如买茶送体质报告）",
            "更新销售话术库（根据昨日客户反馈优化1条）",
        ],
    )
    emp = AIEmployee(config, max_tokens=4096)
    for t in SALES_TOOLS:
        emp.add_tool(t)
    return emp


def follow_up_lead(employee: AIEmployee, lead_info: dict) -> str:
    """跟进一条销售线索"""
    context = f"""客户信息：
- 姓名/昵称：{lead_info.get('name', '未知')}
- 上次咨询：{lead_info.get('last_query', '无')}
- 体质类型：{lead_info.get('constitution', '未测')}
- 是否购买过：{lead_info.get('purchased', '否')}
- 联系方式：{lead_info.get('contact', '无')}

请生成一条跟进消息，目标：引导再次互动或完成首单。"""
    return employee.work("生成客户跟进消息", context=context)
