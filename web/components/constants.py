"""Shared constants: knowledge-base tools, system prompts, constitution quiz, navigation, and the t() helper."""

import streamlit as st
from pathlib import Path
from agents.base import BaseAgent, Tool

# ── Knowledge-base paths ──────────────────────────────────────

_KB = Path(__file__).parent.parent.parent / "data" / "tcm"

def _read(f):
    return (_KB / f).read_text(encoding="utf-8")

# ── TCM knowledge-base tools ──────────────────────────────────

TCM_TOOLS = [
    Tool("read_tcm_basics", "中医基础理论",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("basics.md")),
    Tool("read_tcm_diet", "食疗养生",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("diet_therapy.md")),
    Tool("read_tcm_conditions", "常见症状辨证",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("common_conditions.md")),
    Tool("read_tcm_herbs", "中药学",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("herbs.md")),
    Tool("read_tcm_meridians", "经络穴位",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("meridians.md")),
    Tool("read_tcm_formulas", "经典方剂",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("formulas.md")),
    Tool("read_wuyunliuqi", "五运六气·毛小妹运气医学",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("wuyunliuqi.md")),
    Tool("read_symptom_checker", "症状检查器·症状→证型快速映射",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("symptom_checker.md")),
    Tool("read_body_weather", "人体气象站·毛小妹课程全集",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("body_weather_station.md")),
    Tool("read_mao_practice", "毛小妹实践课·8堂动手实操",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("mao_practice.md")),
    Tool("read_folk_remedies", "民间食疗偏方大全·36个家传小方",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("folk_remedies.md")),
    Tool("read_mianxiang", "周易面相学·五行面型+五色诊+脏腑分区+三停十二宫",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("zhouyi_mianxiang.md")),
    Tool("read_tea_therapy", "茶饮食疗库·25款养生茶配方+体质速查",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("tea_therapy.md")),
    Tool("read_personalized_tea", "五运六气个性化茶饮处方·一人一方·节气茶·地域茶",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("personalized_tea.md")),
    Tool("read_fengshui", "金锁玉关风水学·八卦砂水·二十四山·实战案例",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("jinsuoyuguan.md")),
    Tool("read_student_health", "留学生健康指南·常见问题+平价方案+穴位急救",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("student_health.md")),
    Tool("read_summer_health", "2026夏季养生前沿·九体质辨证·卫健委辟谣",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("summer_health_2026.md")),
    Tool("read_culture_oversea", "中医文化出海·国风趋势·汉服茶道太极",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("culture_出海_2026.md")),
    Tool("read_AI_TCM_news", "AI中医前沿·固生堂·天河灵枢·Jingfang多Agent",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("AI_出海_2026.md")),
    Tool("read_womens_health", "女性健康中医食疗·痛经·月经不调·带下·更年期·艾灸方案",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("womens_health.md")),
    Tool("read_sleep_health", "中医睡眠调理·失眠六证型·分季调理·特殊人群方案",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("sleep_health.md")),
    Tool("read_mental_health", "中医情志调理·七情对应五脏·焦虑抑郁·五行音乐·留学生心理",
         {"type": "object", "properties": {}, "required": []},
         lambda **kw: _read("mental_health.md")),
]

# ── System prompts ────────────────────────────────────────────

SYSTEM_ZH = """你是「妙手堂AI」——山东妙手堂中医诊所的智能健康顾问。专业、精准、温暖。

## 核心能力（24个知识库）
- 四诊合参 + 八纲辨证 + 五运六气 + 周易面诊 + 金锁玉关 + 睡眠调理 + 情志健康
- 症状检查/食疗/中药/经络/方剂/茶饮/偏方/风水/留学生/夏季/女性健康/睡眠/心理健康
- 给个性化的「辨证+食疗+穴位+茶饮+生活方式」五维方案

## 智能问诊流程
1. 接收主诉 → **追问2-3个关键问题**（舌象/睡眠/二便/情绪/疼痛性质 五选三）
2. **自然提议舌诊**：方便就拍照，辨证更精准。不方便继续问诊
3. **首次问诊必问出生年月** → read_wuyunliuqi 分析先天体质+当年运气
4. 用 read_symptom_checker 交叉验证症状 → 确定证型方向
5. **每次回复必含以下6项**：
   📋 **辨证结论**（通俗比喻1句 + 专业辨证术语）
   🔍 **症状分析**（为什么有这个症状，中医怎么解释）
   🍳 **民间食疗小方**（1-2个，含克数+步骤+为什么有效）
   💆 **对症穴位**（1-2个，含精确取穴+按法+时长+禁忌）
   🍵 **推荐茶饮**（从茶饮食疗库匹配1款）
   🥗 **饮食宜忌**（各3条，优先推荐超市常见食材）
6. 结尾附一句话免责

## 回复风格
- 用生活比喻解释中医（「肝火就像水壶烧干了」）
- 辨证专业严谨，建议通俗易懂
- 像朋友聊天，不是教科书

## 铁律
- 所有药材穴位方剂必查知识库，不编造
- 不诊断不处方不替代医生
- 偏方标注「🍳 民间小方」

⚠️ 本内容仅供健康教育参考，不替代医生诊断。"""

SYSTEM_EN = """You are the AI health advisor for Shandong BenCao Tang TCM Clinic, serving international users worldwide.

## Your Identity
- A warm, professional TCM practitioner AI
- Use simple English, explain TCM with everyday analogies
- Friendly and conversational style

## Core Capabilities (18 Knowledge Bases)
- Four-Diagnosis + Pattern Differentiation + Five Movements Six Qi
- Face reading + Tongue diagnosis + Constitution analysis
- Diet therapy + Acupressure + Tea prescription + Folk remedies

## Consultation Flow
1. Receive complaint → Ask 2 follow-up questions (sleep/digestion/emotions/tongue)
2. Gently offer tongue photo option (no pressure)
3. First visit: Ask birth year/month for constitutional analysis
4. Every response MUST include:
   📋 Pattern Diagnosis (plain English + TCM terms)
   🍳 Folk Remedy (ingredients + method + why it works)
   💆 Acupressure (1-2 points with location + technique)
   🍵 Tea Recommendation (from tea therapy library)
   🥗 Diet Advice (eat + avoid, use local supermarket items)

## Rules
- Always consult knowledge bases, never fabricate
- No diagnosis, no prescriptions, not substitute for medical care
- Include appropriate disclaimer

⚠️ Disclaimer: Educational info only. Not medical advice. Consult a qualified healthcare professional."""

# ── Constitution quiz ─────────────────────────────────────────

CONSTITUTION_QUIZ = {
    "平和质": ["精力充沛", "睡眠质量好", "适应能力强"],
    "气虚质": ["容易疲劳气短", "说话声音低弱", "容易出虚汗"],
    "阳虚质": ["手脚发凉", "比一般人怕冷", "吃凉的不舒服"],
    "阴虚质": ["手心脚心发热", "口干咽燥", "容易失眠盗汗"],
    "痰湿质": ["身体沉重不爽快", "腹部肥胖松软", "舌苔厚腻"],
    "湿热质": ["面部出油长痘", "口苦口臭", "大便粘滞"],
    "气郁质": ["情绪低落焦虑", "容易胸闷叹气", "对事情敏感"],
    "血瘀质": ["身上容易瘀青", "面色偏暗有斑", "容易忘事"],
    "特禀质": ["容易过敏", "过敏性鼻炎哮喘", "皮肤起荨麻疹"],
}

# ── Navigation pages ──────────────────────────────────────────

NAV_PAGES = [
    ("home", "🏠", "首页", "Home"),
    ("consult", "💬", "AI 问诊", "AI Consult"),
    ("culture", "🏯", "文化出海", "Culture"),
    ("partners", "🤝", "合伙人", "Partners"),
    ("experts", "👨‍⚕️", "名医团队", "Experts"),
    ("shop", "🛒", "养生商城", "Shop"),
    ("contact", "📞", "联系我们", "Contact"),
    ("dashboard", "📊", "数据后台", "Dashboard"),
]

# ── Translation helper ────────────────────────────────────────

def t(zh, en):
    """Return zh or en based on current language in st.session_state."""
    lang = st.session_state.get("lang", "zh")
    return zh if lang == "zh" else en


def get_label(page_id, zh, en):
    """Localised label for a nav entry."""
    return t(zh, en)
