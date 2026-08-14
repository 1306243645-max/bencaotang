"""AI内容官 — 每日文案、视频脚本、海报创意、社媒运营"""

from pathlib import Path
from datetime import datetime
from agents.base import Tool
from agents.employees.base_employee import AIEmployee, EmployeeConfig

_KB = Path(__file__).parent.parent.parent / "data" / "tcm"

# ── 内容官专用工具 ────────────────────────────────────

def _read(name: str) -> str:
    p = _KB / f"{name}.md"
    if p.exists():
        return p.read_text(encoding="utf-8")[:3000]
    return ""

CONTENT_TOOLS = [
    Tool("kb_tea", "茶饮食疗库·25款配方", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("tea_therapy")),
    Tool("kb_folk", "民间偏方·36个小方", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("folk_remedies")),
    Tool("kb_culture", "中医文化出海·国风趋势", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("culture_出海_2026")),
    Tool("kb_summer", "2026夏季养生前沿", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("summer_health_2026")),
    Tool("kb_womens", "女性健康中医食疗", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("womens_health")),
    Tool("kb_sleep", "中医睡眠调理·失眠六证型", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("sleep_health")),
    Tool("kb_mental", "中医情志调理·焦虑抑郁", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("mental_health")),
    Tool("kb_exercises", "传统养生功法·八段锦五禽戏太极易筋经", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("health_exercises")),
    Tool("kb_solar", "二十四节气养生·四时食疗·冬病夏治", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("solar_terms_health")),
    Tool("kb_beauty", "中医美容养颜·内调外养·七白面膜", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("beauty_skincare")),
    Tool("kb_classics", "中医经典著作与国学文化", {"type":"object","properties":{},"required":[]},
         lambda **kw: _read("classics_culture")),
]

# ── 内容官系统提示词 ──────────────────────────────────

CONTENT_OFFICER_PROMPT = """你是妙手堂的AI内容官「文白」——负责所有对外内容的策划和创作。

## 你的身份
- 懂中医、懂传播、懂用户心理的内容专家
- 文风多变：科普时专业严谨，朋友圈时亲切温暖，小红书时会抓眼球
- 每条内容必须有「知识点 + 情绪价值 + 行动引导」

## 你的职责
1. **每日文案**：朋友圈/公众号/小红书各1条
2. **视频脚本**：60秒口播脚本（含画面描述+口播词+标签）
3. **海报创意**：海报主题+文案+视觉建议
4. **热点借势**：结合节气、节日、热点创作内容
5. **系列策划**：睡眠周/脾胃周/女性健康周等内容专题

## 内容日历
- 周一：AI问诊体验 → 引流体质测试
- 周二：茶饮食疗 → 产品推广
- 周三：国风文化 → 汉服/太极/茶道
- 周四：穴位教学 → 关注引流
- 周五：用户反馈 → 信任建设
- 周六：节气养生 → 转发裂变
- 周日：一周总结 → 合伙人招募

## 内容公式
每条文案 = 痛点提问(1句) + 中医解释(2-3句) + 实用建议(1-2条) + 引流引导(1句)
视频脚本 = 0-5s钩子 + 5-25s干货 + 25-40s产品/方法 + 40-50s行动号召 + 50-60s品牌露出

## 铁律
- 不夸大疗效
- 不制造焦虑
- 每条内容带免责声明或引流引导
- 数据引用要准确（查知识库）"""


def create_content_officer() -> AIEmployee:
    """创建AI内容官"""
    config = EmployeeConfig(
        name="文白",
        role="AI内容官",
        emoji="✍️",
        system_prompt=CONTENT_OFFICER_PROMPT,
        daily_tasks=[
            "生成今日朋友圈文案（根据内容日历主题）",
            "生成今日小红书图文（标题+正文+标签）",
            "生成今日短视频脚本（60秒口播+画面描述）",
            "生成今日养生日签一句话",
            "策划明天的内容主题和方向",
        ],
    )
    emp = AIEmployee(config, max_tokens=4096)
    for t in CONTENT_TOOLS:
        emp.add_tool(t)
    return emp


def generate_daily_content(employee: AIEmployee, weekday_theme: str = None) -> dict:
    """生成今日全套内容"""
    today = datetime.now()
    themes = ["AI问诊体验", "茶饮食疗", "国风文化", "穴位教学", "用户反馈", "节气养生", "合伙人招募"]
    theme = weekday_theme or themes[today.weekday()]

    result = employee.work(f"""
今天是{today.strftime('%Y年%m月%d日')}，周{today.strftime('%A')}，内容主题：「{theme}」

请生成以下内容（JSON格式）：

{{
  "wechat_post": "朋友圈/公众号文案（150字）",
  "xiaohongshu": {{"title": "吸引人的标题", "body": "正文100字+标签"}},
  "video_script": "60秒视频脚本（含时间轴+画面+口播）",
  "daily_tip": "一句养生日签（20字）",
  "hashtags": ["标签1", "标签2", "标签3"]
}}

要求：每条结尾引导「微信搜妙手堂免费测体质」""")
    return result
