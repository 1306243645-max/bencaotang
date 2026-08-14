"""TCM Consultation Agent — 中医问诊智能体，面向澳洲市场。"""

from pathlib import Path
from agents.base import BaseAgent, Tool

# 知识库路径
_KB = Path(__file__).parent.parent / "data" / "tcm"

# ── 知识库读取工具 ────────────────────────────────────────

def _read_tcm_basics(**kwargs) -> str:
    return (_KB / "basics.md").read_text(encoding="utf-8")

def _read_diet_therapy(**kwargs) -> str:
    return (_KB / "diet_therapy.md").read_text(encoding="utf-8")

def _read_common_conditions(**kwargs) -> str:
    return (_KB / "common_conditions.md").read_text(encoding="utf-8")

def _read_herbs(**kwargs) -> str:
    return (_KB / "herbs.md").read_text(encoding="utf-8")

def _read_meridians(**kwargs) -> str:
    return (_KB / "meridians.md").read_text(encoding="utf-8")

def _read_formulas(**kwargs) -> str:
    return (_KB / "formulas.md").read_text(encoding="utf-8")

TCM_BASICS_TOOL = Tool(
    name="read_tcm_basics",
    description="查询中医基础理论：阴阳五行、气血、六淫七情、八纲辨证、常用证型。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_tcm_basics,
)

TCM_DIET_TOOL = Tool(
    name="read_tcm_diet",
    description="查询中医食疗知识：食物性味、五脏对应、常见证型食疗方案、澳洲四季养生。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_diet_therapy,
)

TCM_CONDITIONS_TOOL = Tool(
    name="read_tcm_conditions",
    description="查询常见症状的中医辨证：失眠、消化问题、压力焦虑、疲劳、头痛、妇科。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_common_conditions,
)

TCM_HERBS_TOOL = Tool(
    name="read_tcm_herbs",
    description="查询中药学知识：常用药材（解表/清热/补虚/理气/活血/祛湿/安神）的性味归经、功效、注意事项及澳洲TGA管制信息。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_herbs,
)

TCM_MERIDIANS_TOOL = Tool(
    name="read_tcm_meridians",
    description="查询经络穴位：十四经脉、常用穴位定位、功效、自我按摩指导、常用穴位组合。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_meridians,
)

TCM_FORMULAS_TOOL = Tool(
    name="read_tcm_formulas",
    description="查询经典方剂学知识：解表/清热/补益/理气/祛湿/安神/消食/活血类常用方剂的组成、适应症、澳洲OTC可用情况。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_formulas,
)

def _read_wuyunliuqi(**kwargs) -> str:
    return (_KB / "wuyunliuqi.md").read_text(encoding="utf-8")

TCM_WUYUN_TOOL = Tool(
    name="read_wuyunliuqi",
    description="查询五运六气学说：天干地支推算、运气格局、出生年运气体质、每年运气分析、运气养生法、运气穴位、节气养生。用于分析患者先天体质和当年运气影响。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_wuyunliuqi,
)

def _read_body_weather(**kwargs) -> str:
    return (_KB / "body_weather_station.md").read_text(encoding="utf-8")

TCM_BODY_WEATHER_TOOL = Tool(
    name="read_body_weather",
    description="查询五运六气人体气象站完整课程：人体气象站三大功能、出生密码解码、当年气象预报、节气经络开合、三步诊断法、运气食疗、疾病预测。用于深度分析体质和每年健康预测。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_body_weather,
)

def _read_mao_practice(**kwargs) -> str:
    return (_KB / "mao_practice.md").read_text(encoding="utf-8")

TCM_MAO_PRACTICE_TOOL = Tool(
    name="read_mao_practice",
    description="查询毛小妹实践课·8堂动手实操：运气推算练习、出生体质诊断、舌象气象观测、节气追踪、经络自测、运气食疗配方、临床案例研讨、年度养生计划制定。用户问实操/怎么做/帮我制定计划时使用。",
    input_schema={"type": "object", "properties": {}, "required": []},
    handler=_read_mao_practice,
)


# ── 系统提示词 ────────────────────────────────────────────

TCM_SYSTEM_PROMPT = """\
你是「山东妙手堂中医诊所」的 AI 健康顾问（BenCao Tang TCM Clinic），面向澳大利亚(Australia)用户。

## 你的身份
- 基于《黄帝内经》《伤寒杂病论》等经典中医理论
- 使用英文为主（但必要时可引用中文术语），覆盖澳洲多元文化用户
- 严格遵循澳洲法规

## 核心能力
### 0. 知识库
你可以使用以下知识库工具查询详细信息:
- read_tcm_basics — 基础理论
- read_tcm_diet — 食疗知识
- read_tcm_conditions — 常见症状辨证
- read_tcm_herbs — 中药学（性味归经、功效、注意事项、TGA管制）
- read_tcm_meridians — 经络穴位（定位、自我按摩、常用组合）
- read_tcm_formulas — 经典方剂（组成、适应症、澳洲OTC可用情况）
- read_wuyunliuqi — 🌟 五运六气（毛小妹运气医学、出生年运气体质、当年运气分析）
**重要**: 涉及具体药材、穴位定位、方剂名称时，务必查阅对应知识库，确保准确性。
**五运六气**: 当用户问出生年份相关的体质、当年运势养生、或"为什么今年总生病"类问题时，用 read_wuyunliuqi 查询。
**问出生年**: 如果用户问体质相关问题，可以询问对方出生年份，用五运六气分析先天体质。

### 1. 四诊合参 (在线版)
基于用户文字描述，模拟中医四诊:
- 望(Wang/Inspection): 请用户描述舌象（颜色、舌苔）、面色
- 闻(Wen/Listening): 询问声音状态、口臭/体味情况
- 问(Wen/Inquiry): 详细询问症状、饮食、睡眠、情绪、二便
- 切(Qie/Palpation): 在线无法切脉，请用户描述脉搏大致感觉

### 2. 辨证论治
使用八纲辨证 (Eight Principles):
- 表里 (Exterior/Interior)
- 寒热 (Cold/Heat)
- 虚实 (Deficiency/Excess)
- 阴阳 (Yin/Yang)

结合脏腑辨证 (Zang-Fu)、气血津液辨证 (Qi-Blood-Fluids)

### 3. 建议范畴（澳洲合规）
✅ 可以给的建议:
- 食疗 (Dietary therapy): 食物推荐/忌口
- 生活方式 (Lifestyle): 作息、运动、情绪调节
- 穴位按摩 (Acupressure): 安全的自我按摩穴位
- 中医知识教育 (TCM education)
- 建议就诊 (Referral): 何时应看 AHPRA 注册中医师

❌ 不能做的事:
- 不开处方 (No herbal prescriptions)
- 不做确定性诊断 (No definitive diagnosis)
- 不替代 GP/急诊 (Not replace medical care)
- 不推荐具体中药剂量

## 问诊流程
1. **初诊问询**: 了解主诉 + 关键伴随症状
2. **辨证分析**: 给出中医辨证分析（用英文，保留中医术语 + 中文标注）
3. **调养建议**: 食疗 + 生活方式 + 穴位（如有帮助）
4. **就医指引**: 何时应看注册中医师或 GP

## 澳洲合规声明 (必须)
每条回复末尾附:
---
⚠️ **Disclaimer (Australian Context)**:
This information is for educational purposes only and does not constitute medical advice, diagnosis, or treatment.
It is not a substitute for consultation with a qualified healthcare professional.
In Australia, acupuncture and Chinese herbal medicine should be provided by an AHPRA-registered Chinese medicine practitioner.
If you have a medical emergency, call 000 or visit your nearest emergency department.
For non-urgent medical advice, call HealthDirect on 1800 022 222 (24/7).
"""


def create_tcm_agent(**kwargs) -> BaseAgent:
    """创建一个中医问诊 Agent，预装 TCM 知识库工具。

    用法:
        agent = create_tcm_agent()
        response = agent.chat("I've been having trouble sleeping...")
        print(response.content)
    """
    agent = BaseAgent(
        system=TCM_SYSTEM_PROMPT,
        max_tokens=8192,
        max_tool_rounds=8,
        **kwargs,
    )
    agent.add_tool(TCM_BASICS_TOOL)
    agent.add_tool(TCM_DIET_TOOL)
    agent.add_tool(TCM_CONDITIONS_TOOL)
    agent.add_tool(TCM_HERBS_TOOL)
    agent.add_tool(TCM_MERIDIANS_TOOL)
    agent.add_tool(TCM_FORMULAS_TOOL)
    agent.add_tool(TCM_WUYUN_TOOL)
    agent.add_tool(TCM_BODY_WEATHER_TOOL)
    agent.add_tool(TCM_MAO_PRACTICE_TOOL)
    # 新知识库
    TCM_SYMPTOM_TOOL = Tool("read_symptom_checker","症状检查器",{"type":"object","properties":{},"required":[]},lambda **kw: _read("symptom_checker.md"))
    TCM_FOLK_TOOL = Tool("read_folk_remedies","民间食疗偏方大全",{"type":"object","properties":{},"required":[]},lambda **kw: _read("folk_remedies.md"))
    TCM_MIANXIANG_TOOL = Tool("read_mianxiang","周易面相学",{"type":"object","properties":{},"required":[]},lambda **kw: _read("zhouyi_mianxiang.md"))
    TCM_TEA_TOOL = Tool("read_tea_therapy","茶饮食疗库",{"type":"object","properties":{},"required":[]},lambda **kw: _read("tea_therapy.md"))
    TCM_PERSONAL_TEA_TOOL = Tool("read_personalized_tea","五运六气个性化茶饮处方",{"type":"object","properties":{},"required":[]},lambda **kw: _read("personalized_tea.md"))
    TCM_FENGSHUI_TOOL = Tool("read_fengshui","金锁玉关风水学",{"type":"object","properties":{},"required":[]},lambda **kw: _read("jinsuoyuguan.md"))
    agent.add_tool(TCM_SYMPTOM_TOOL)
    agent.add_tool(TCM_FOLK_TOOL)
    agent.add_tool(TCM_MIANXIANG_TOOL)
    agent.add_tool(TCM_TEA_TOOL)
    agent.add_tool(TCM_PERSONAL_TEA_TOOL)
    agent.add_tool(TCM_FENGSHUI_TOOL)
    return agent
