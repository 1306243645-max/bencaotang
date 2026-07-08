"""山东本草堂中医诊所 · BenCao Tang TCM Clinic — 官网"""

import sys, json, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from datetime import datetime
from agents.base import BaseAgent, Tool

# ── 知识库 ────────────────────────────────────────────────

_KB = Path(__file__).parent.parent / "data" / "tcm"
def _read(f): return (_KB / f).read_text(encoding="utf-8")

TCM_TOOLS = [
    Tool("read_tcm_basics","中医基础理论",{"type":"object","properties":{},"required":[]},lambda **kw:_read("basics.md")),
    Tool("read_tcm_diet","食疗养生",{"type":"object","properties":{},"required":[]},lambda **kw:_read("diet_therapy.md")),
    Tool("read_tcm_conditions","常见症状辨证",{"type":"object","properties":{},"required":[]},lambda **kw:_read("common_conditions.md")),
    Tool("read_tcm_herbs","中药学",{"type":"object","properties":{},"required":[]},lambda **kw:_read("herbs.md")),
    Tool("read_tcm_meridians","经络穴位",{"type":"object","properties":{},"required":[]},lambda **kw:_read("meridians.md")),
    Tool("read_tcm_formulas","经典方剂",{"type":"object","properties":{},"required":[]},lambda **kw:_read("formulas.md")),
    Tool("read_wuyunliuqi","五运六气·毛小妹运气医学",{"type":"object","properties":{},"required":[]},lambda **kw:_read("wuyunliuqi.md")),
    Tool("read_symptom_checker","症状检查器·症状→证型快速映射",{"type":"object","properties":{},"required":[]},lambda **kw:_read("symptom_checker.md")),
    Tool("read_body_weather","人体气象站·毛小妹课程全集",{"type":"object","properties":{},"required":[]},lambda **kw:_read("body_weather_station.md")),
    Tool("read_mao_practice","毛小妹实践课·8堂动手实操",{"type":"object","properties":{},"required":[]},lambda **kw:_read("mao_practice.md")),
    Tool("read_folk_remedies","民间食疗偏方大全·36个家传小方",{"type":"object","properties":{},"required":[]},lambda **kw:_read("folk_remedies.md")),
    Tool("read_mianxiang","周易面相学·五行面型+五色诊+脏腑分区+三停十二宫",{"type":"object","properties":{},"required":[]},lambda **kw:_read("zhouyi_mianxiang.md")),
    Tool("read_tea_therapy","茶饮食疗库·25款养生茶配方+体质速查",{"type":"object","properties":{},"required":[]},lambda **kw:_read("tea_therapy.md")),
    Tool("read_personalized_tea","五运六气个性化茶饮处方·一人一方·节气茶·地域茶",{"type":"object","properties":{},"required":[]},lambda **kw:_read("personalized_tea.md")),
    Tool("read_fengshui","金锁玉关风水学·八卦砂水·二十四山·实战案例",{"type":"object","properties":{},"required":[]},lambda **kw:_read("jinsuoyuguan.md")),
    Tool("read_student_health","留学生健康指南·常见问题+平价方案+穴位急救",{"type":"object","properties":{},"required":[]},lambda **kw:_read("student_health.md")),
]

# ── 系统提示词 ────────────────────────────────────────────

SYSTEM_ZH = """你是「小妙」——山东本草堂中医诊所的AI健康顾问。温暖亲切，专业严谨。

## 核心能力
- 四诊合参 + 八纲九候 + 五运六气 + 周易面诊 + 金锁玉关风水
- 16个知识库随时查阅：症状检查/食疗/中药/经络/方剂/五运六气/人体气象站/偏方/茶饮/风水
- 给个性化的食疗+穴位+茶饮+生活方式方案

## 问诊流程
1. 接收主诉 → **追问1-2个关键问题**（睡眠/二便/情绪至少问一个）
2. **自然提议舌诊**：「方便的话可以拍张舌头照片，我帮你看得更准。不方便也没关系～」
   - 用户愿意 → 引导拍自然光下舌头照片 → 结合舌象辨证
   - 用户不愿意 → 直接继续问诊，不强迫
3. **首次问诊主动询问出生年月** → 五运六气分析先天体质
4. 用知识库交叉验证 → 给出精准辨证
5. 每次回复**必含以下4项**：
   📋 **辨证结论**（通俗版1句话 + 专业辨证）
   🍳 **民间食疗小方**（1-2个，含食材+做法+原理）
   💆 **对症穴位**（1-2个，含位置+按摩方法）
   🥗 **饮食宜忌**（3-5条）
6. 结尾附一句话免责

## 留学生特别模式
- 碰到留学生/学生用户，优先推荐平价方案（超市食材+免费穴位）
- 理解留学场景：赶due熬夜、外卖胃、咖啡续命、考试焦虑
- 用 read_student_health 知识库获取针对性方案
- 强调「留学生也能轻松做到」的低成本调理

## 回复风格
- 像朋友聊天，用生活比喻（「肝火就像锅烧干了」）
- 辨证专业，建议通俗
- 适当用 ✨🐼💡 表情

## 规则
- 所有药材穴位方剂必须查知识库，不可编造
- 不诊断不处方不替代医生
- 偏方标注「🍳 民间小方」
- 每条回复末尾附免责

⚠️ 本内容仅供健康教育参考，不替代医生诊断。"""

SYSTEM_EN = """You are the AI advisor for Shandong BenCao Tang TCM Clinic, serving Australian users.
Capabilities: Four-Diagnosis, pattern differentiation, diet/acupressure/lifestyle advice. Always consult knowledge base.
No prescriptions, no definitive diagnosis, not medical care substitute. Include AU disclaimer.
⚠️ Disclaimer: Educational info only. Consult AHPRA-registered practitioner. Emergency: 000. HealthDirect: 1800 022 222."""

# ── 体质问卷 ──────────────────────────────────────────────

CONSTITUTION_QUIZ = {
    "平和质":["精力充沛","睡眠质量好","适应能力强"],
    "气虚质":["容易疲劳气短","说话声音低弱","容易出虚汗"],
    "阳虚质":["手脚发凉","比一般人怕冷","吃凉的不舒服"],
    "阴虚质":["手心脚心发热","口干咽燥","容易失眠盗汗"],
    "痰湿质":["身体沉重不爽快","腹部肥胖松软","舌苔厚腻"],
    "湿热质":["面部出油长痘","口苦口臭","大便粘滞"],
    "气郁质":["情绪低落焦虑","容易胸闷叹气","对事情敏感"],
    "血瘀质":["身上容易瘀青","面色偏暗有斑","容易忘事"],
    "特禀质":["容易过敏","过敏性鼻炎哮喘","皮肤起荨麻疹"],
}

# ── 诊所信息 ──────────────────────────────────────────────

CLINIC_INFO = {
    "name": "山东本草堂中医诊所",
    "name_en": "Shandong BenCao Tang TCM Clinic",
    "slogan": "本草济世 · 仁心济世",
    "slogan_en": "Healing Hands · Compassionate Care",
    "address": "山东省济南市历下区经十路123号",
    "phone": "+86 18254191315",
    "wechat": "18254191315",
    "email": "83497212@qq.com",
    "hours": "周一至周五 8:30-17:30 | 周六 9:00-16:00",
    "description": "本草堂源于山东中医世家，三代传承，立足齐鲁大地，服务全国。我们结合经典中医理论与现代健康理念，为广大群众提供专业、温暖的中医健康服务。",
}

# ── 页面配置 ──────────────────────────────────────────────

st.set_page_config(page_title="本草堂中医诊所", page_icon="🐼", layout="wide")

# ── CSS ───────────────────────────────────────────────────

st.markdown("""<style>
    /* ═══════════ 本草堂 · 宋式美学 装饰版 ═══════════ */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;700&family=Noto+Sans+SC:wght@300;400;500&family=ZCOOL+XiaoWei&display=swap');
    * { font-family: 'Noto Sans SC', 'PingFang SC', sans-serif !important; }

    :root {
        --accent: #9B8EC4; --accent-light: #B5A8D4; --accent-pale: #EDE8F5;
        --accent-dark: #7B6EA4; --bamboo: #C4B5A5; --rice: #FAF8FC;
        --rice-dark: #F2EEF6; --ink-light: #8C8C8C; --ink: #5C5C5C;
        --ink-dark: #3C3C3C; --mist: #D9D2E6; --petal: #E0D8EB;
        --gold: #C9A96E;
    }

    /* ═══ 全局背景——宣纸纹理 ═══ */
    .stApp, .main {
        background-color: #FAF8FC !important;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(155,142,196,0.04) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(201,169,110,0.04) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(155,142,196,0.03) 0%, transparent 70%);
        background-attachment: fixed;
    }

    /* ═══ 侧边栏——柔紫 ═══ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F2FA 0%, #EEE8F5 50%, #F5F2FA 100%) !important;
        border-right: 1px solid var(--mist) !important;
        box-shadow: 2px 0 12px rgba(0,0,0,0.03) !important;
    }
    section[data-testid="stSidebar"] * { color: var(--ink) !important; }
    section[data-testid="stSidebar"] h2 {
        font-family: 'Noto Serif SC','ZCOOL XiaoWei',serif !important;
        font-weight:500 !important; letter-spacing:0.08em !important;
        text-align:center !important;
    }
    section[data-testid="stSidebar"] h4 {
        font-weight:400 !important; letter-spacing:0.06em !important;
        position:relative; padding-bottom:0.5rem;
    }
    section[data-testid="stSidebar"] h4::after {
        content:''; position:absolute; bottom:0; left:0;
        width:30px; height:2px; background:var(--accent); border-radius:1px;
    }
    section[data-testid="stSidebar"] .stMetric {
        background: white !important; border:1px solid var(--accent-light) !important;
        border-radius:12px !important; box-shadow:0 1px 4px rgba(0,0,0,0.03) !important;
    }

    /* ═══ 导航 ═══ */
    .nav-btn {
        display:inline-block; padding:0.5rem 1.2rem;
        background: white; color: var(--ink) !important; font-weight:400;
        text-align:center; cursor:pointer; transition:all 0.3s;
        text-decoration:none; font-size:0.9rem; letter-spacing:0.05em;
        border:1px solid var(--accent-light); border-radius:20px;
        box-shadow:0 1px 3px rgba(0,0,0,0.03);
    }
    .nav-btn:hover { background: var(--accent-pale); border-color: var(--accent); transform:translateY(-1px); }
    .nav-btn.active { background: var(--accent); color: white !important; border-color: var(--accent); box-shadow:0 2px 8px rgba(155,142,196,0.3); }

    /* ═══ Hero ═══ */
    .hero {
        text-align:center; padding:4.5rem 2rem; position:relative; overflow:hidden;
        background: linear-gradient(180deg, #EDE8F5 0%, #F3EFF7 30%, #F8F5FB 60%, #FAF8FC 100%);
        border-bottom: 1px solid var(--accent-light); margin-bottom:2rem;
    }
    .hero::before {
        content:''; position:absolute; top:0; left:50%; transform:translateX(-50%);
        width:60px; height:3px; background: linear-gradient(90deg,transparent,var(--accent),transparent);
        border-radius:2px;
    }
    .hero::after {
        content:''; position:absolute; top:20%; right:10%;
        width:120px; height:120px; border-radius:50%;
        background:radial-gradient(circle, rgba(155,142,196,0.08) 0%, transparent 70%);
    }
    .hero h1 {
        font-size:2.4rem; font-weight:300; letter-spacing:0.15em;
        position:relative; display:inline-block;
    }
    .hero h1::after {
        content:''; position:absolute; bottom:-8px; left:50%; transform:translateX(-50%);
        width:40px; height:2px; background:var(--accent); border-radius:1px;
    }
    .hero p { font-size:1.05rem; color: var(--ink-light); font-weight:300; }

    /* ═══ 卡片 ═══ */
    .service-card {
        background: white; border-radius:16px; padding:2rem;
        box-shadow:0 1px 3px rgba(0,0,0,0.03); height:100%;
        border:1px solid #F0EBE8; transition:all 0.3s; position:relative;
        overflow:hidden;
    }
    .service-card::before {
        content:''; position:absolute; top:0; left:0; right:0; height:3px;
        background: linear-gradient(90deg, var(--accent), var(--accent-light));
        opacity:0; transition:opacity 0.3s;
    }
    .service-card:hover::before { opacity:1; }
    .service-card:hover {
        box-shadow:0 8px 24px rgba(0,0,0,0.06);
        border-color: var(--accent-light); transform:translateY(-2px);
    }
    .service-card h4 { color:var(--ink-dark); font-size:1.05rem; font-weight:500; letter-spacing:0.04em; }
    .service-card:hover h4 { color: var(--accent-dark); }

    /* ═══ 页脚 ═══ */
    .footer {
        text-align:center; padding:3rem 2rem; color:var(--ink-light);
        font-size:0.85rem; margin-top:3rem; font-weight:300;
        border-top:1px solid var(--mist);
        background: linear-gradient(180deg, #FAF8FC, #F5F2FA);
        position:relative;
    }
    .footer::before {
        content:''; position:absolute; top:0; left:50%; transform:translateX(-50%);
        width:80px; height:2px; background: linear-gradient(90deg,transparent,var(--accent-light),transparent);
    }

    /* ═══ 分割线装饰 ═══ */
    hr { border:none; border-top:1px solid var(--mist); margin:2rem 0; position:relative; }
    hr::after {
        content:'◆'; position:absolute; top:-10px; left:50%; transform:translateX(-50%);
        color:var(--accent-light); font-size:0.5rem; background:#FAF8FC; padding:0 0.5rem;
    }

    /* ═══ 按钮 ═══ */
    .stButton button {
        border-radius:24px !important; font-weight:400 !important;
        letter-spacing:0.05em !important; transition:all 0.3s !important;
        background: linear-gradient(135deg, var(--accent), var(--accent-dark)) !important;
        color: white !important; border:none !important;
        padding:0.55rem 1.8rem !important; box-shadow:0 2px 8px rgba(155,142,196,0.25) !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #8B7EB4, #6B5E94) !important;
        transform:translateY(-1px) !important; box-shadow:0 4px 16px rgba(155,142,196,0.35) !important;
    }

    /* ═══ 聊天 ═══ */
    .stChatMessage { border-radius:16px !important; border:1px solid #F0EBE8 !important; box-shadow:0 1px 3px rgba(0,0,0,0.02) !important; }
    .stChatMessage [data-testid="stChatMessageContent"] { padding:1.2rem 1.5rem !important; line-height:1.8 !important; }

    /* ═══ 指标卡 ═══ */
    .stMetric {
        background:white !important; border-radius:12px !important;
        border:1px solid var(--accent-light) !important;
        box-shadow:0 1px 4px rgba(0,0,0,0.03) !important;
    }

    /* ═══ Tab ═══ */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom:1px solid var(--mist) !important; gap:0.3rem;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight:400 !important; color:var(--ink-light) !important;
        letter-spacing:0.04em !important; border-radius:20px 20px 0 0 !important;
        background: transparent !important; border:none !important;
        padding:0.5rem 1.3rem !important; transition:all 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent) !important; font-weight:500 !important;
        border-bottom:2px solid var(--accent) !important;
        background: rgba(155,142,196,0.04) !important;
    }

    /* ═══ 输入框 ═══ */
    .stChatInput textarea {
        border-radius:24px !important; border:1.5px solid var(--mist) !important;
        padding:0.8rem 1.2rem !important; transition:all 0.3s !important;
    }
    .stChatInput textarea:focus {
        border-color: var(--accent) !important;
        box-shadow:0 0 0 3px rgba(155,142,196,0.12) !important;
    }

    /* ═══ 展开面板 ═══ */
    .stExpander {
        border:1px solid var(--mist) !important; border-radius:12px !important;
        box-shadow:0 1px 3px rgba(0,0,0,0.02) !important;
    }

    /* ═══ 选择框 ═══ */
    .stSelectbox [data-baseweb="select"] { border-radius:12px !important; border-color:var(--mist) !important; }

    /* ═══ 淡入动画 ═══ */
    @keyframes fadeIn {
        from { opacity:0; transform:translateY(12px); }
        to { opacity:1; transform:translateY(0); }
    }
    .service-card { animation: fadeIn 0.5s ease-out; }
    .hero h1 { animation: fadeIn 0.6s ease-out; }
    .hero p { animation: fadeIn 0.8s ease-out; }
</style>""", unsafe_allow_html=True)

# ── 初始化 ────────────────────────────────────────────────

if "lang" not in st.session_state: st.session_state.lang = "zh"
if "page" not in st.session_state: st.session_state.page = "home"
if "messages" not in st.session_state: st.session_state.messages = []
if "tool_count" not in st.session_state: st.session_state.tool_count = 0
if "bookings" not in st.session_state: st.session_state.bookings = []
if "cart" not in st.session_state: st.session_state.cart = []
if "orders" not in st.session_state: st.session_state.orders = []
if "ref" not in st.session_state: st.session_state.ref = st.query_params.get("ref","")
if "shares" not in st.session_state: st.session_state.shares = 0

if "agent" not in st.session_state:
    system = SYSTEM_ZH if st.session_state.lang=="zh" else SYSTEM_EN
    agent = BaseAgent(system=system,max_tokens=8192,max_tool_rounds=8)
    for t in TCM_TOOLS: agent.add_tool(t)
    st.session_state.agent = agent

L = st.session_state.lang

# ── 辅助函数 ──────────────────────────────────────────────

def t(zh, en):
    return zh if L == "zh" else en

def switch_lang(lang):
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        system = SYSTEM_ZH if lang=="zh" else SYSTEM_EN
        agent = BaseAgent(system=system,max_tokens=8192,max_tool_rounds=8)
        for t in TCM_TOOLS: agent.add_tool(t)
        st.session_state.agent = agent
        st.rerun()

# ── 顶部导航 ─────────────────────────────────────────────

nav_pages = [
    ("home", "🏠", t("首页","Home")),
    ("about", "📖", t("关于我们","About")),
    ("services", "🩺", t("诊疗服务","Services")),
    ("recipes", "🍲", t("食疗食谱","Recipes")),
    ("shop", "🛒", t("养生商城","Shop")),
    ("consult", "💬", t("AI 问诊","AI Consult")),
    ("contact", "📞", t("预约联系","Contact")),
    ("dashboard", "📊", t("数据后台","Dashboard")),
]

cols_nav = st.columns([0.3] + [1]*len(nav_pages) + [0.3])
for i, (page_id, icon, label) in enumerate(nav_pages):
    with cols_nav[i+1]:
        cls = "nav-btn active" if st.session_state.page == page_id else "nav-btn"
        if st.button(f"{icon} {label}", key=f"nav_{page_id}", use_container_width=True):
            st.session_state.page = page_id
            st.rerun()

st.divider()

# ── 侧边栏（全局） ────────────────────────────────────────

with st.sidebar:
    st.markdown(f"## 🐼 本草堂")
    # 熊猫萌宠
    import base64 as _b64
    _img = _b64.b64encode(open('web/static/orange_cat.png','rb').read()).decode()
    st.markdown(f"""
    <div style="text-align:center;padding:0.5rem;margin:0.5rem 0;background:rgba(255,255,255,0.06);border-radius:12px;border:1px solid rgba(155,142,196,0.3);">
        <img src="data:image/png;base64,{_img}" width="130" style="border-radius:50%;">
        <div style="font-weight:700;color:#B5A8D4;font-size:1rem;margin-top:0.3rem;">妙妙 · Panda</div>
        <div style="font-size:0.75rem;opacity:0.7;">本草堂 AI 健康问诊</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(t("三代传承 · 正宗中医","Heritage TCM · Since 1980s"))
    st.divider()
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("🇨🇳 中文", use_container_width=True, type="primary" if L=="zh" else "secondary"): switch_lang("zh")
    with col_r:
        if st.button("🇦🇺 EN", use_container_width=True, type="primary" if L=="en" else "secondary"): switch_lang("en")
    st.divider()
    st.markdown(f"**📞** {CLINIC_INFO['phone']}")
    st.markdown(f"**📧** {CLINIC_INFO['email']}")
    st.markdown(f"**💬** 微信：{CLINIC_INFO['wechat']}")
    st.divider()
    # ── 社交媒体矩阵 ──
    st.markdown(f"#### 🌐 社交媒体")
    social_html = """
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;justify-content:center;">
    <a href="https://weibo.com/本草堂" target="_blank" style="background:#E6162D;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🧣 微博</a>
    <a href="https://xiaohongshu.com/本草堂" target="_blank" style="background:#FE2C55;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📕 小红书</a>
    <a href="https://douyin.com/本草堂" target="_blank" style="background:#111;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🎵 抖音</a>
    <a href="https://facebook.com/BenCaoTang" target="_blank" style="background:#1877F2;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📘 FB</a>
    <a href="https://instagram.com/bencaotang_tcm" target="_blank" style="background:#E4405F;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📷 IG</a>
    <a href="https://tiktok.com/@bencaotang" target="_blank" style="background:#000;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🎬 TikTok</a>
    </div>
    """
    st.markdown(social_html, unsafe_allow_html=True)
    st.divider()
    # ── 本草堂二维码（高容错+白边）──
    st.markdown(f"#### 📱 {t('扫码打开本草堂','Scan for BenCao Tang')}")
    import io, qrcode, base64 as b64
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

    mst_url = "https://wet-camels-sit.loca.lt"
    try:
        qr = qrcode.QRCode(
            version=None,  # 自动大小
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # 高容错 30%
            box_size=12,
            border=4,  # 白边
        )
        qr.add_data(mst_url)
        qr.make(fit=True)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="#2d6a4f",
            back_color="white",
        )
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        qr_b64_img = b64.b64encode(buf.getvalue()).decode()
        st.markdown(f'<div style="text-align:center;background:white;padding:12px;border-radius:12px;display:inline-block;"><img src="data:image/png;base64,{qr_b64_img}" width="180"></div>', unsafe_allow_html=True)
    except Exception:
        # 降级方案：普通二维码
        qr_img = qrcode.make(mst_url)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        qr_b64_img = b64.b64encode(buf.getvalue()).decode()
        st.markdown(f'<div style="text-align:center"><img src="data:image/png;base64,{qr_b64_img}" width="180"></div>', unsafe_allow_html=True)

    st.caption(f"📱 {t('微信扫码打开本草堂官网','Scan with WeChat to open')}")
    st.caption(f"🔗 {t('公网链接','Public URL')}: wet-camels-sit.loca.lt")
    st.caption(t("💡 扫码不成功？试试截图→微信扫一扫→相册","💡 Can't scan? Screenshot → WeChat → Album"))

    # 推荐追踪
    st.divider()
    st.markdown(f"#### 🎯 {t('推荐有礼','Referral Program')}")
    if st.session_state.ref:
        st.success(t(f"🎉 来自推荐: {st.session_state.ref}","🎉 Referred by: "+st.session_state.ref))
    st.metric(t("今日分享","Shares Today"), st.session_state.shares)
    st.caption(t("每推荐1位好友 → 双方各得免费体质茶1份","Refer a friend → Both get free tea"))
    st.divider()
    st.caption("© 2026 山东本草堂中医诊所")

# ═══════════════════════════════════════════════════════════
# 🏠 首页
# ═══════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown(f"""
    <div class="hero">
        <p style="font-size:0.9rem;color:#B5D3C5;letter-spacing:0.2em;text-transform:uppercase;">SHANDONG MIAOSHOU TANG</p>
        <h1>山东本草堂</h1>
        <p style="font-size:1.3rem;color:var(--accent);font-weight:300;margin:0.5rem 0;">{CLINIC_INFO['slogan']}</p>
        <p style="font-style:italic;color:var(--ink-light);font-weight:300;margin-top:1.5rem;font-size:0.95rem;">
        「上医治未病」 ——《黄帝内经》
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 装饰分隔
    st.markdown("""
    <div style="text-align:center;padding:1rem 0;">
        <span style="color:#D9D2E6;font-size:1.2rem;letter-spacing:0.3em;">◆ ◇ ◆</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {t('本堂特色','Our Heritage')}")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="service-card"><h4>🌿 ' + t('三代中医传承','Heritage TCM') + '</h4><p>' + t('山东中医世家，三代人专注中医诊疗，将正宗的中医智慧带到澳大利亚。','Three generations of TCM practitioners bringing authentic Chinese medicine to Australia.') + '</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="service-card"><h4>🤖 ' + t('AI + 中医','AI + TCM') + '</h4><p>' + t('自研 AI 问诊系统，24/7 在线健康咨询，智能体质辨识，让中医触手可及。','AI-powered health advisor available 24/7 for TCM consultation and constitution analysis.') + '</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="service-card"><h4>🇦🇺 ' + t('澳洲合规','AU Registered') + '</h4><p>' + t('AHPRA 注册中医师执业，TGA 合规药材，Medibank/Bupa 可报销。','AHPRA-registered practitioners, TGA-compliant herbs, private health fund rebates available.') + '</p></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### {t('📊 快速开始','📊 Quick Start')}")
    cq1,cq2,cq3 = st.columns(3)
    with cq1:
        if st.button(t("👅 AI 舌诊分析","👅 Tongue Diagnosis"), use_container_width=True):
            st.session_state.page = "consult"; st.rerun()
    with cq2:
        if st.button(t("📋 体质自测","📋 Constitution Test"), use_container_width=True):
            st.session_state.page = "consult"; st.rerun()
    with cq3:
        if st.button(t("💬 在线问诊","💬 AI Consultation"), use_container_width=True):
            st.session_state.page = "consult"; st.rerun()

# ═══════════════════════════════════════════════════════════
# 📖 关于我们
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    st.markdown(f"## 📖 {t('关于本草堂','About BenCao Tang')}")
    st.divider()

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown(f"""
        ### {t('我们的故事','Our Story')}

        {t(
        '山东本草堂中医诊所，源自齐鲁大地，三代中医世家传承。创始人张老先生上世纪 80 年代在山东济南创立本草堂，以"本草济世、仁心济世"为堂训，服务一方百姓。',
        'Shandong BenCao Tang TCM Clinic traces its roots to Jinan, Shandong Province, where the founding family has practiced Chinese medicine for three generations since the 1980s.'
        )}

        {t(
        '第二代传人在家传基础上，融汇现代医学理念，将本草堂发展为集针灸、中药、推拿、食疗为一体的综合性中医诊所。',
        'The second generation integrated modern medical knowledge with traditional wisdom, expanding the clinic into a comprehensive TCM practice covering acupuncture, herbal medicine, tuina massage, and dietary therapy.'
        )}

        {t(
        '如今，第三代传人将本草堂带到澳大利亚悉尼，致力于为澳洲华人社区及本地居民提供正宗、专业、温暖的中医健康服务。我们结合 AI 技术，让传统中医更加便捷、精准。',
        'Today, the third generation brings BenCao Tang to Sydney, Australia, dedicated to providing authentic, professional, and compassionate TCM care to the Chinese community and local residents. We leverage AI technology to make traditional medicine more accessible and precise.'
        )}
        """)

        # 中医经典
    st.markdown(f"### 📜 {t('医道传承','TCM Heritage')}")
    st.markdown(f"""
    <div style="background:white;border:1px solid #E8F2ED;border-radius:12px;padding:2rem;margin:1rem 0;text-align:center;">
        <p style="color:#8DB6A5;font-style:italic;font-size:1.1rem;font-weight:300;line-height:2;">
        「阴阳者，天地之道也，万物之纲纪。」<br>
        <span style="font-size:0.8rem;color:#B5D3C5;">——《黄帝内经·素问》</span>
        </p>
        <p style="color:#8C8C8C;font-size:0.9rem;font-weight:300;margin-top:1rem;">
        「夫医者，非仁爱不可托也」 —— 杨泉《物理论》
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {t('执业资质','Credentials')}")
    st.markdown(t(
        "- ✅ AHPRA 注册中医师\n- ✅ CMBA 认证\n- ✅ 私人医保可报销\n- ✅ TGA 合规中药",
        "- ✅ AHPRA Registered\n- ✅ CMBA Certified\n- ✅ Health Fund Rebates\n- ✅ TGA Compliant"
    ))

    with col_b:
        st.markdown("### 🕐 " + t("应诊时间","Hours"))
        st.info(CLINIC_INFO["hours"])
        st.markdown("### 📍 " + t("诊所地址","Address"))
        st.info(CLINIC_INFO["address"])

# ═══════════════════════════════════════════════════════════
# 🩺 诊疗服务
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "services":
    st.markdown(f"## 🩺 {t('诊疗服务','Our Services')}")
    st.divider()

    services = [
        ("💉", t("针灸治疗","Acupuncture"), t("传统毫针、电针、温针、耳针，治疗疼痛、失眠、消化问题、妇科调理等。","Traditional acupuncture for pain, insomnia, digestion, gynecology & more.")),
        ("🐼", t("中药调理","Herbal Medicine"), t("个性化方剂，散剂/汤剂/丸剂，TGA 合规药材。","Personalized herbal formulas, powders, decoctions & pills with TGA-compliant herbs.")),
        ("💆", t("推拿按摩","Tuina Massage"), t("中医推拿正骨、经络疏通，缓解颈肩腰腿痛。","Therapeutic tuina for musculoskeletal pain, meridian疏通 & relaxation.")),
        ("🔥", t("艾灸拔罐","Moxibustion & Cupping"), t("温经散寒、祛湿通络，改善寒性体质。","Warming meridians, dispelling cold & dampness, improving constitution.")),
        ("🥗", t("食疗养生","Dietary Therapy"), t("根据体质定制食疗方案，用澳洲本地食材调养身体。","Customized dietary plans using Australian ingredients based on your TCM constitution.")),
        ("👅", t("AI 舌诊体质分析","AI Tongue & Constitution Analysis"), t("自研 AI 系统，上传舌象照片+自测问卷，智能评估体质类型。","AI-powered tongue image analysis and constitution assessment.")),
    ]

    for icon, title, desc in services:
        st.markdown(f'<div class="service-card" style="margin-bottom:1rem;"><h4>{icon} {title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# 💬 AI 问诊
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "consult":
    tab_names = [t("💬 智能问诊","💬 Chat"), t("👅 舌诊分析","👅 Tongue"), t("🔮 面诊分析","🔮 Face"), t("🏔️ 风水咨询","🏔️ Feng Shui"), t("🍵 问茶","🍵 Tea"), t("📋 体质自测","📋 Quiz")]
    tab_chat, tab_tongue, tab_mianxiang, tab_fengshui, tab_teapres, tab_quiz = st.tabs(tab_names)

    # --- 智能问诊 ---
    with tab_chat:
        if not st.session_state.messages:
            st.markdown(f"### {t('欢迎使用本草堂 AI 问诊','Welcome to BenCao Tang AI')}")
            st.markdown(t(
                "我是本草堂的 AI 健康顾问。请描述你的症状，我将从中医角度帮你分析。\n\n📸 方便的话上传舌头照片，辨证更精准。不方便也没关系～\n\n⚠️ 本 AI 提供健康教育信息，不替代医生诊断。",
                "I'm the BenCao Tang AI health advisor. Describe your symptoms for TCM analysis.\n\n📸 Optional: upload a tongue photo for more accurate diagnosis.\n\n⚠️ Educational info only."
            ))
            st.caption(t("💡 试试：失眠口干怎么办 | 饭后腹胀乏力 | 月经痛怕冷","💡 Try: insomnia, bloating, period pain..."))

            # 留学生快捷入口
            stu_col1, stu_col2, stu_col3 = st.columns(3)
            with stu_col1:
                if st.button(t("🎓 留学生熬夜救急","🎓 Student Burnout"), use_container_width=True, key="stu1"):
                    st.session_state.messages.append({"role":"user","content":"我是留学生，经常熬夜赶due，喝很多咖啡，现在失眠口干，有什么平价调理方法？"})
                    st.rerun()
            with stu_col2:
                if st.button(t("📚 考试焦虑调理","📚 Exam Stress"), use_container_width=True, key="stu2"):
                    st.session_state.messages.append({"role":"user","content":"留学生考试压力大，焦虑紧张，有什么中医方法可以缓解？要简单便宜的。"})
                    st.rerun()
            with stu_col3:
                if st.button(t("🍜 外卖胃求救","🍜 Poor Diet Fix"), use_container_width=True, key="stu3"):
                    st.session_state.messages.append({"role":"user","content":"留学生天天吃外卖，胃不舒服，腹胀便秘，有什么超市就能买到的调理方法？"})
                    st.rerun()

        # 舌诊上传（嵌入聊天区，可选）
        tongue_file = st.file_uploader(
            t("📸 上传舌象照片（可选，拍了辨证更准）","📸 Upload tongue photo (optional)"),
            type=["jpg","jpeg","png","webp"], key="tongue_chat", label_visibility="visible"
        )
        if tongue_file:
            if st.button(t("🔍 分析舌象并加入问诊","🔍 Analyze"), use_container_width=True):
                with st.spinner(t("分析舌象中...","Analyzing...")):
                    tp = t("从中医角度分析舌象：舌色舌形苔色苔质。简短回复。","TCM tongue analysis: color shape coating. Brief.")
                    resp = st.session_state.agent.chat(tp)
                    st.session_state.messages.append({"role":"user","content":"📸 [上传了舌象照片]"})
                    st.session_state.messages.append({"role":"assistant","content":f"👅 {resp.content}"})
                    st.success(t("舌象已分析！请继续描述症状","Tongue analyzed! Continue describing"))
                    st.rerun()

        for msg in st.session_state.messages:
            avatar = "🧑" if msg["role"]=="user" else "🐼"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        if prompt := st.chat_input(t("描述你的症状...","Describe your symptoms...")):
            st.session_state.messages.append({"role":"user","content":prompt})
            with st.chat_message("user", avatar="🧑"): st.markdown(prompt)
            with st.chat_message("assistant", avatar="🐼"):
                try:
                    with st.spinner(t("辨证分析中...","Analyzing pattern...")):
                        # 构建对话历史传给 Agent
                        history = []
                        for m in st.session_state.messages[:-1]:  # 不包括刚发的这条
                            role = "user" if m["role"] == "user" else "assistant"
                            history.append({"role": role, "content": m["content"]})
                        resp = st.session_state.agent.chat(prompt, history=history if history else None)
                        st.markdown(resp.content)
                        st.session_state.tool_count += len(resp.tool_calls or [])
                        # 显示工具调用统计
                        if resp.tool_calls:
                            st.caption(f"📚 调用了 {len(resp.tool_calls)} 个知识库")
                except Exception as e:
                    st.error(f"错误: {type(e).__name__}: {e}")
                    import traceback
                    st.code(traceback.format_exc())
            st.session_state.messages.append({"role":"assistant","content":resp.content if 'resp' in dir() else '系统出错，请重试'})

        if st.session_state.messages:
            st.divider()
            if st.button(t("🔄 新对话","🔄 New Chat"), use_container_width=True):
                st.session_state.messages = []; st.session_state.tool_count = 0; st.rerun()

    # --- 舌诊分析 ---
    with tab_tongue:
        st.markdown(f"### 👅 {t('舌诊分析','Tongue Diagnosis')}")
        st.info(t("📸 自然光拍摄，不美颜，舌头自然伸出","📸 Natural light, no filter, tongue extended naturally"))
        tongue_file = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="tongue")
        if tongue_file:
            c_i, c_b = st.columns([1,1])
            with c_i: st.image(tongue_file, use_container_width=True, caption="Tongue Image")
            with c_b:
                if st.button(t("🔍 分析舌象","🔍 Analyze"), use_container_width=True, type="primary"):
                    with st.spinner(t("分析中...","Analyzing...")):
                        prompt = t(
                            "从中医角度分析舌象：舌色、舌形、苔色、苔质四个维度。给出综合辨证+食疗+穴位建议。附澳洲免责。",
                            "TCM tongue analysis: color, shape, coating color, coating texture. Give pattern impression + diet + acupressure. Include AU disclaimer."
                        )
                        resp = st.session_state.agent.chat(prompt)
                        st.markdown(resp.content)
                        st.session_state.messages.append({"role":"user","content":"👅 [舌象照片]"})
                        st.session_state.messages.append({"role":"assistant","content":resp.content})

    # --- 体质自测 ---
    with tab_quiz:
        st.markdown(f"### 📋 {t('体质自测','Constitution Self-Test')}")
        st.caption(t("1=从不 2=很少 3=有时 4=经常 5=总是","1=Never 2=Rarely 3=Sometimes 4=Often 5=Always"))
        scores = {}
        ctype_keys = list(CONSTITUTION_QUIZ.keys())
        for idx, ctype in enumerate(ctype_keys):
            qs = CONSTITUTION_QUIZ[ctype]
            st.markdown(f"**{ctype}**")
            cols = st.columns(len(qs))
            vals = []
            for i, q in enumerate(qs):
                safe_key = f"qz_{idx}_{i}"
                with cols[i]: vals.append(st.select_slider(q,[1,2,3,4,5],3,key=safe_key,label_visibility="collapsed"))
            scores[ctype]=vals

        c_a, c_b = st.columns([1,4])
        with c_a:
            if st.button(t("📊 查看结果","📊 View Results"), use_container_width=True, type="primary"):
                results = {ct:round(sum(v)/len(v),1) for ct,v in scores.items()}
                sorted_r = sorted(results.items(), key=lambda x:x[1], reverse=True)
                st.divider()
                top = sorted_r[0]
                st.success(f"**{top[0]}** ({top[1]}/5)")
                for ct, sc in sorted_r:
                    st.markdown(f"**{ct}**: {sc}/5")
                    st.progress(sc/5)
                top_types = [f"{ct}:{s}" for ct,s in sorted_r if s>=3.0]
                with st.spinner(t("分析中...","Analyzing...")):
                    resp = st.session_state.agent.chat(
                        f"用户体质自测：{', '.join(top_types)}。请给出体质特点、食疗建议（澳洲食材）、穴位按摩、生活调整。附澳洲免责。")
                    st.markdown(resp.content)
                st.session_state.messages.append({"role":"user","content":f"📋 体质自测: {', '.join(top_types)}"})
                st.session_state.messages.append({"role":"assistant","content":resp.content})
        with c_b:
            if st.button(t("🔄 重置","🔄 Reset"), use_container_width=True):
                for ci in range(len(ctype_keys)):
                    for i in range(3): st.session_state.pop(f"qz_{ci}_{i}", None)
                st.rerun()

    # --- 金锁玉关风水咨询 ---
    with tab_fengshui:
        st.markdown(f"### 🏔️ {t('金锁玉关 · 风水咨询','Jin Suo Yu Guan Feng Shui')}")
        st.caption(t("八卦砂水法 · 二十四山向 · 家居风水诊断","8-Trigram Sand-Water Method"))

        feng_col1, feng_col2 = st.columns([1,1])
        with feng_col1:
            feng_type = st.selectbox(t("咨询类型","Type"), [
                t("家居风水","Home"),t("办公室风水","Office"),t("健康风水","Health"),t("事业财运","Career")
            ], key="feng_type")
            feng_issue = st.selectbox(t("主要问题","Main Issue"), [
                t("睡眠不好","Poor Sleep"),t("事业不顺","Career Issues"),t("家人健康","Family Health"),
                t("财运不佳","Financial"),t("孩子学业","Children Studies"),t("人际关系","Relationships"),
                t("综合诊断","General Check")
            ], key="feng_issue")
        with feng_col2:
            feng_dir = st.text_input(t("房屋朝向（如坐北朝南）","House Direction"), placeholder=t("例如：坐北朝南","e.g. North-South"), key="feng_dir")
            feng_desc = st.text_area(t("房屋布局描述","Layout Description"), placeholder=t("例如：西北方是厨房，正南是落地窗，正东是卫生间...","e.g. NW=kitchen, S=window, E=bathroom..."), key="feng_desc", height=100)

        if st.button(t("🏔️ 风水诊断","🏔️ Feng Shui Analysis"), use_container_width=True, type="primary"):
            if feng_dir or feng_desc:
                with st.spinner(t("金锁玉关分析中...","Analyzing Feng Shui...")):
                    prompt = f"""用户咨询金锁玉关风水：
类型={feng_type}，问题={feng_issue}
朝向={feng_dir or '未提供'}，布局={feng_desc or '未提供'}

请用 read_fengshui 知识库进行分析：

1. 🧭 八卦砂水诊断（逐方位分析砂水是否得位）
2. ⚠️ 找出问题方位（砂水反位的地方）
3. 🩺 对应的健康/运势影响
4. 🔧 具体化解方案（每个问题方位给出可操作的化解方法）
5. 📋 综合风水评分和改进建议"""
                    resp = st.session_state.agent.chat(prompt)
                    st.markdown(resp.content)
                    st.session_state.messages.append({"role":"user","content":f"🏔️ 风水咨询：{feng_type}"})
                    st.session_state.messages.append({"role":"assistant","content":resp.content})
            else:
                st.warning(t("请至少填写房屋朝向或布局描述","Please fill in at least direction or layout"))

    # --- 问茶（五运六气茶饮处方）---
    with tab_teapres:
        st.markdown(f"### 🍵 {t('五运六气 · 一人一茶','Personalized Tea Rx')}")
        st.caption(t("出生体质 + 当前节气 + 所在地域 → 今日专属茶方","Birth constitution + Solar term + Location = Your Tea"))

        tea_col1, tea_col2 = st.columns([1,1])
        with tea_col1:
            from datetime import datetime as _dt
            tea_birth = st.date_input(
                t("出生日期","Birth Date"),
                value=_dt(1990, 6, 15),
                min_value=_dt(1940, 1, 1),
                max_value=_dt(2026, 12, 31),
                key="tea_birth"
            )
        with tea_col2:
            tea_location = st.selectbox(t("所在地","Location"), [
                t("北方（黄河以北）","North"),t("南方（长江以南）","South"),
                t("东部沿海","East Coast"),t("西部高原","West"),t("中部（中原）","Central"),
                t("东北","Northeast"),t("西南","Southwest"),t("海外·澳洲","Australia")
            ], key="tea_loc")
            today = _dt.now()
            st.info(f"📅 {t('今日','Today')}: {today.strftime('%Y年%m月%d日')}")
            st.caption(t("💡 出生月日定位六气时段，体质分析更精准","Birth MD → Qi phase, more precise"))

        if st.button(t("🍵 生成今日专属茶方","🍵 Generate My Tea"), use_container_width=True, type="primary"):
            with st.spinner(t("正在推算您的专属茶方...","Creating your tea prescription...")):
                prompt = f"""用户信息：
- 出生日期：{tea_birth.year}年{tea_birth.month}月{tea_birth.day}日
- 所在地：{tea_location}
- 当前日期：{today.strftime('%Y-%m-%d')}

请用 read_personalized_tea 知识库，结合毛小妹五运六气和人体气象站理论，为这个用户生成「一人一方」专属茶饮处方。

注意：
- 出生月日能更精准判断司天/在泉的影响权重
- 生于上半年受司天影响大，下半年受在泉影响大
- 月日落在不同节气（初之气到终之气）影响不同

输出格式：
1. 🎯 先天运气体质分析（根据出生年月日推算，含岁运+司天在泉权重）
2. 📅 当前节气影响（自动判断当前属于哪个节气）
3. 🌍 地域调和茶材
4. 🍵 **今日专属茶方**（含具体配方克数+泡法）
5. 💪 功效说明
6. ⚠️ 禁忌提醒"""
                resp = st.session_state.agent.chat(prompt)
                st.markdown(resp.content)
                st.session_state.messages.append({"role":"user","content":f"🍵 问茶：{tea_birth.year}年{tea_birth.month}月{tea_birth.day}日生，{tea_location}"})
                st.session_state.messages.append({"role":"assistant","content":resp.content})

    # --- 面诊分析 ---
    with tab_mianxiang:
        st.markdown(f"### 🔮 {t('周易面诊分析','Zhouyi Face Reading')}")
        st.info(t("📸 自然光正面照，不美颜，可以看到全脸","📸 Natural light, front-facing photo, no filter"))

        face_col1, face_col2 = st.columns([1,1])
        with face_col1:
            face_type = st.selectbox(t("你的面型（对着镜子看）","Face Shape"),
                [t("方形（国字脸）","Square"),t("长形（长脸）","Long"),t("圆形（满月脸）","Round"),
                 t("三角形（甲字脸）","Triangle"),t("梯形（由字脸）","Trapezoid")])
            face_color = st.selectbox(t("整体面色","Complexion"),
                [t("正常红润","Normal"),t("偏青","Bluish"),t("偏红","Reddish"),
                 t("偏黄","Yellowish"),t("偏白","Pale"),t("偏黑/暗","Dark")])
            mian_areas = st.multiselect(t("面部异常区域（多选）","Problem Areas"),
                [t("额头痘痘/红赤","Forehead"),t("眉心发红","Between brows"),
                 t("鼻头发红","Nose tip"),t("两颧潮红","Cheek flush"),
                 t("眼眶暗沉","Dark circles"),t("下巴反复长痘","Chin acne"),
                 t("太阳穴青筋","Temple veins"),t("嘴唇苍白","Pale lips")])

        with face_col2:
            mian_age = st.number_input(t("年龄","Age"), 15, 90, 30)
            mian_sleep = st.selectbox(t("睡眠质量","Sleep"), [t("好","Good"),t("一般","OK"),t("差","Poor")])
            mian_stress = st.selectbox(t("压力程度","Stress"), [t("低","Low"),t("中","Medium"),t("高","High")])

            if st.button(t("🔮 周易面诊分析","🔮 Analyze Face"), use_container_width=True, type="primary"):
                with st.spinner(t("面诊分析中...","Analyzing face...")):
                    prompt = f"""请用周易面相结合中医望诊进行分析：

用户信息：面型={face_type}，面色={face_color}，年龄={mian_age}岁
面部问题：{', '.join(mian_areas) if mian_areas else '无明显异常'}
睡眠={mian_sleep}，压力={mian_stress}

请给出：
1. 🎭 五行面型分析（面型对应五行+体质倾向）
2. 🎨 五色诊分析（面色对应脏腑问题）
3. 🗺️ 面部区域分析（每个异常区域对应的脏腑问题）
4. 📋 综合面诊结论
5. 🍳 对应调理建议（食疗+穴位+生活方式）
6. ⚠️ 附免责声明

使用 read_mianxiang 知识库。"""
                    resp = st.session_state.agent.chat(prompt)
                    st.markdown(resp.content)
                    st.session_state.messages.append({"role":"user","content":f"🔮 面诊分析：面型{face_type}，面色{face_color}"})
                    st.session_state.messages.append({"role":"assistant","content":resp.content})

    # 侧栏统计
    with st.sidebar:
        st.divider()
        st.metric(t("消息","Msgs"), len(st.session_state.messages)//2)
        st.metric(t("知识库调用","KB Uses"), st.session_state.tool_count)

        # 引流磁铁
        st.divider()
        st.markdown(f"#### 🎁 {t('免费领体质报告','Free Report')}")
        lead_email = st.text_input(t("输入邮箱获取完整体质报告","Email for free report"), key="lead_email")
        if st.button(t("📩 发送报告","📩 Send Report"), use_container_width=True, type="primary"):
            if lead_email and "@" in lead_email and st.session_state.messages:
                # 保存线索
                lead_file = Path(__file__).parent.parent / "output" / "leads.jsonl"
                lead_file.parent.mkdir(exist_ok=True)
                import json as _json
                with open(lead_file, "a", encoding="utf-8") as f:
                    _json.dump({"email": lead_email, "time": datetime.now().isoformat()}, f, ensure_ascii=False)
                    f.write("\n")
                st.success(t("✅ 报告已发送！请查收邮箱","✅ Report sent! Check your inbox"))
            elif not lead_email:
                st.error(t("请输入邮箱","Enter email"))
            else:
                st.error(t("请先进行问诊再领取报告","Chat first then get report"))

# ═══════════════════════════════════════════════════════════
# 🍲 食疗食谱
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "recipes":
    st.markdown(f"## 🍲 {t('食疗食谱库','Dietary Therapy Recipes')}")
    st.caption(t("30道实用食疗方 · 澳洲食材 · 简单易做","30 TCM recipes using Australian ingredients"))
    st.divider()

    recipe_cats = {
        "🍵 茶饮类": ["菊花枸杞明目茶","玫瑰红枣养颜茶","陈皮生姜暖胃茶","桂圆红枣安神茶","薏米赤小豆祛湿茶","山楂麦芽消食茶","银耳百合润肺羹","黑芝麻核桃糊"],
        "🍲 汤品类": ["四神汤","当归生姜羊肉汤","玉竹沙参润肺汤","花旗参石斛汤","茯苓白术健脾汤","杜仲牛膝强骨汤","枸杞猪肝明目汤","冬瓜薏米排骨汤"],
        "🥣 粥品类": ["小米红枣养胃粥","山药芡实健脾粥","黑米桂圆补血粥","百合莲子安神粥","薏米赤小豆祛湿粥","核桃黑芝麻补肾粥"],
        "🍯 膏方零食": ["秋梨膏","阿胶糕","八珍糕","桑葚膏"],
        "🦶 泡脚外用": ["艾叶生姜泡脚方","红花当归活血泡脚方","安神助眠泡脚方","祛湿止痒泡脚方"],
    }

    # 加载食谱数据
    recipes_data = {}
    try:
        recipe_text = _read("recipes.md")
        current_recipe = None
        for line in recipe_text.split("\n"):
            line = line.strip()
            if line.startswith("### ") and line[4].isdigit():
                current_recipe = line.split(" ", 2)[-1] if " " in line else line[4:]
                recipes_data[current_recipe] = {"title": current_recipe, "lines": []}
            elif current_recipe and line:
                recipes_data[current_recipe]["lines"].append(line)
    except Exception:
        pass

    # 茶饮食疗Tab
    st.markdown(f"### 🍵 {t('茶饮食疗库','Tea Therapy Library')}")
    tea_tabs_list = [t("安神助眠","Sleep"),t("清肝明目","Eye"),t("健脾祛湿","Spleen"),t("补气养血","Blood"),t("美容养颜","Beauty"),t("四季养生","Season"),t("减肥消脂","Slim")]
    tea_cats = [
        ["酸枣仁安神茶","桂圆红枣安神茶","玫瑰花安神茶","莲子心竹叶清心茶"],
        ["菊花枸杞明目茶","桑叶菊花清肝茶","决明子山楂降脂茶"],
        ["陈皮茯苓祛湿茶","生姜红枣暖胃茶","山药芡实健脾茶","大麦消食茶"],
        ["黄芪当归补血茶","党参桂圆补气茶","五红补血茶","黑芝麻核桃茶"],
        ["玫瑰柠檬养颜茶","银耳雪梨润肤茶","桃花养颜茶","薏仁美白茶"],
        ["春·疏肝升阳茶","夏·清暑祛湿茶","秋·润肺生津茶","冬·温阳暖身茶"],
        ["荷叶山楂减肥茶","普洱茶消脂茶"],
    ]
    tea_tabs = st.tabs(tea_tabs_list)
    for tab, items in zip(tea_tabs, tea_cats):
        with tab:
            for item in items:
                with st.expander(f"🍵 {item}"):
                    if item in recipes_data:
                        st.markdown("\n".join(recipes_data[item]["lines"]))
                    else:
                        st.caption(t("详情请查看 tea_therapy.md","See tea_therapy.md"))

    st.divider()
    for tab, (cat_name, items) in zip(tabs, recipe_cats.items()):
        with tab:
            for item in items:
                with st.expander(item):
                    if item in recipes_data:
                        content = "\n".join(recipes_data[item]["lines"])
                        # 简单格式化
                        for kw in ["功效","适合","食材","做法","禁忌","售价"]:
                            content = content.replace(f"- **{kw}**:", f"\n**{kw}**：")
                        st.markdown(content)
                    else:
                        st.caption(t("食谱详情请查看完整文件","See recipes.md for details"))


# ═══════════════════════════════════════════════════════════
# 🛒 养生商城
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "shop":
    st.markdown(f"## 🛒 {t('养生食品商城','Wellness Shop')}")
    st.caption(t("本草堂精选 · 药食同源 · 澳洲配送","BenCao Tang精选 · Food-as-Medicine · AU Delivery"))
    st.divider()

    products = [
        {"name": "菊花枸杞茶包", "price": "$12", "desc": "清肝明目，10包装", "tag": "🔥 热销", "img": "🍵"},
        {"name": "玫瑰红枣养颜茶", "price": "$15", "desc": "疏肝养血，10包装", "tag": "💝 女性必备", "img": "🌹"},
        {"name": "四神汤料包", "price": "$12", "desc": "健脾祛湿，4人份", "tag": "👨‍👩‍👧‍👦 全家适用", "img": "🍲"},
        {"name": "秋梨膏", "price": "$25", "desc": "润肺止咳，250g/瓶", "tag": "🍂 秋季必囤", "img": "🍯"},
        {"name": "黑芝麻核桃粉", "price": "$20", "desc": "补肾乌发，300g/罐", "tag": "💪 男士推荐", "img": "🥜"},
        {"name": "阿胶糕", "price": "$35", "desc": "补血养颜，250g/盒", "tag": "👸 口碑爆款", "img": "🍬"},
        {"name": "安神助眠泡脚包", "price": "$15", "desc": "宁心安神，5次量", "tag": "😴 失眠救星", "img": "🦶"},
        {"name": "艾叶生姜泡脚包", "price": "$10", "desc": "温经散寒，7次量", "tag": "❄️ 冬季必备", "img": "🔥"},
        {"name": "陈皮生姜暖胃茶", "price": "$10", "desc": "温中散寒，10包装", "tag": "👍 口碑好", "img": "🫚"},
        {"name": "花旗参石斛汤料", "price": "$25", "desc": "益气养阴，4人份", "tag": "⭐ 高端滋补", "img": "💎"},
        {"name": "八珍糕", "price": "$18", "desc": "健脾养胃，12块/盒", "tag": "👶 老少皆宜", "img": "🍰"},
        {"name": "桑葚膏", "price": "$22", "desc": "滋阴补血，250g/瓶", "tag": "💆 养发", "img": "🫐"},
    ]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1.2rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:1rem;text-align:center;">
                <div style="font-size:3rem;">{p['img']}</div>
                <span style="background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:1rem;font-size:0.75rem;">{p['tag']}</span>
                <h4 style="margin:0.5rem 0;">{p['name']}</h4>
                <p style="color:#6b7280;font-size:0.85rem;">{p['desc']}</p>
                <p style="font-size:1.3rem;font-weight:700;color:#2d6a4f;">{p['price']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("🛒 加入购物车","🛒 Add to Cart"), key=f"cartbtn_{i}", use_container_width=True):
                st.session_state.cart.append(p["name"])
                st.toast(f"✅ {p['name']}")

    # 购物车
    st.divider()
    st.markdown(f"### 🛒 {t('购物车','Shopping Cart')} ({len(st.session_state.cart)})")
    if st.session_state.cart:
        from collections import Counter
        cart_items = Counter(st.session_state.cart)
        for item, qty in cart_items.items():
            c1,c2 = st.columns([4,1])
            c1.markdown(f"**{item}** x{qty}")
            if c2.button(t("删除","Remove"), key=f"rm_{item}"):
                st.session_state.cart.remove(item)
                st.rerun()
        if st.button(t("🗑️ 清空购物车","🗑️ Clear Cart"), use_container_width=True):
            st.session_state.cart = []
            st.rerun()
        # 下单表单
        st.markdown("---")
        st.markdown(f"### 📝 {t('提交订单','Submit Order')}")
        order_name = st.text_input(t("姓名","Name"), key="order_name")
        order_phone = st.text_input(t("电话","Phone"), key="order_phone")
        order_addr = st.text_area(t("收货地址","Delivery Address"), key="order_addr")
        if st.button(t("✅ 确认下单","✅ Place Order"), use_container_width=True, type="primary"):
            if order_name and order_phone:
                order = {
                    "name": order_name, "phone": order_phone, "address": order_addr,
                    "items": dict(cart_items), "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.orders.append(order)
                # 保存到文件
                order_file = Path(__file__).parent.parent / "output" / "orders.jsonl"
                order_file.parent.mkdir(exist_ok=True)
                with open(order_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(order, ensure_ascii=False) + "\n")
                st.session_state.cart = []
                st.success(t("✅ 订单已提交！我们将尽快联系您确认。","✅ Order submitted! We'll contact you shortly."))
                st.balloons()
            else:
                st.error(t("请填写姓名和电话。","Please fill in name and phone."))
    else:
        st.caption(t("购物车空空，去逛逛吧~","Your cart is empty."))

    # 支付方式
    st.divider()
    st.markdown(f"### 💰 {t('支付方式','Payment')}")
    pay_col1, pay_col2 = st.columns(2)
    with pay_col1:
        st.markdown(f"**{t('微信支付','WeChat Pay')}**")
        try:
            import qrcode, io, base64 as b64
            pay_qr = qrcode.make(f"wxp://f2f0x7I7K7jMlylC_lhQWtbMfYsBntF1nXWe")
            buf = io.BytesIO(); pay_qr.save(buf, format='PNG')
            st.image(buf, width=160, caption=t("扫一扫付款","Scan to Pay"))
        except Exception: st.info(t("微信支付二维码","WeChat Pay QR"))
    with pay_col2:
        st.markdown(f"**{t('支付宝','Alipay')}**")
        try:
            ali_qr = qrcode.make(f"https://qr.alipay.com/fkx18545vbw4lmq8qlnxe66")
            buf2 = io.BytesIO(); ali_qr.save(buf2, format='PNG')
            st.image(buf2, width=160, caption=t("扫一扫付款","Scan to Pay"))
        except Exception: st.info(t("支付宝二维码","Alipay QR"))
    st.caption(t("💡 付款后截图发给微信 {wechat} 确认订单","💡 Send payment screenshot to WeChat {wechat}").format(wechat=CLINIC_INFO['wechat']))

    st.divider()
    st.markdown(f"### {t('📦 其他购买方式','Other Ways to Order')}")
    c1,c2,c3 = st.columns(3)
    c1.markdown(f"**1️⃣ {t('微信下单','WeChat Order')}**\n\n{t('添加微信直接下单','Add WeChat to order')}: {CLINIC_INFO['wechat']}")
    c2.markdown(f"**2️⃣ {t('电话订购','Phone Order')}**\n\n{t('拨打','Call')}: {CLINIC_INFO['phone']}")
    c3.markdown(f"**3️⃣ {t('到店选购','Visit Us')}**\n\n{CLINIC_INFO['address']}")

# ═══════════════════════════════════════════════════════════
# 📞 预约联系
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "contact":
    st.markdown(f"## 📞 {t('预约联系','Book an Appointment')}")
    st.divider()

    col_form, col_info = st.columns([3, 2])

    with col_form:
        st.markdown(f"### {t('在线预约','Online Booking')}")
        name = st.text_input(t("姓名","Name"))
        email = st.text_input(t("邮箱","Email"))
        phone = st.text_input(t("电话","Phone"))
        service = st.selectbox(t("服务项目","Service"), [
            t("针灸治疗","Acupuncture"),
            t("中药调理","Herbal Medicine"),
            t("推拿按摩","Tuina Massage"),
            t("艾灸拔罐","Moxibustion & Cupping"),
            t("食疗咨询","Dietary Consultation"),
            t("体质评估","Constitution Assessment"),
        ])
        date = st.date_input(t("预约日期","Preferred Date"))
        notes = st.text_area(t("备注（可选）","Notes (optional)"), placeholder=t("描述你的主要症状或需求...","Describe your main concerns..."))

        if st.button(t("✅ 提交预约","✅ Submit Booking"), use_container_width=True, type="primary"):
            if name and email:
                booking = {
                    "name": name, "email": email, "phone": phone,
                    "service": service, "date": str(date), "notes": notes,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.bookings.append(booking)
                # 保存到文件
                booking_file = Path(__file__).parent.parent / "output" / "bookings.jsonl"
                booking_file.parent.mkdir(exist_ok=True)
                with open(booking_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(booking, ensure_ascii=False) + "\n")
                st.success(t(
                    "✅ 预约已提交！我们将在 24 小时内通过电话或微信与您确认。",
                    "✅ Booking submitted! We'll confirm via phone or WeChat within 24 hours."
                ))
            else:
                st.error(t("请填写姓名和邮箱。","Please fill in name and email."))

    with col_info:
        st.markdown(f"### {t('联系方式','Contact Info')}")
        st.markdown(f"""
        **📞 {t('电话','Phone')}**
        {CLINIC_INFO['phone']}

        **📧 {t('邮箱','Email')}**
        {CLINIC_INFO['email']}

        **💬 {t('微信','WeChat')}**
        {CLINIC_INFO['wechat']}

        **📍 {t('地址','Address')}**
        {CLINIC_INFO['address']}

        **🕐 {t('应诊时间','Hours')}**
        {CLINIC_INFO['hours']}
        """)
        st.info(t("💡 首次就诊建议提前15分钟到达，填写健康问卷。","💡 Please arrive 15 minutes early for your first visit."))

# ═══════════════════════════════════════════════════════════
# 📊 数据后台 + 今日推广
# ═══════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    # ── 今日推广面板 ──
    st.markdown("## 📢 " + t("今日推广文案","Todays Content"))
    today_file = Path(__file__).parent.parent / "output" / "auto" / f"today_{datetime.now():%Y%m%d}.json"
    if today_file.exists():
        import json as _json
        data = _json.loads(today_file.read_text(encoding="utf-8"))
        content_str = data.get("content", "")
        # 提取各平台内容
        import re as _re
        wx_match = _re.search(r'wechat_post.*?"(.*?)"', content_str, _re.DOTALL)
        video_match = _re.search(r'video_script.*?"(.*?)"', content_str, _re.DOTALL)
        xhs_match = _re.search(r'xiaohongshu.*?"title".*?"(.*?)".*?"body".*?"(.*?)"', content_str, _re.DOTALL)
        tip_match = _re.search(r'daily_tip.*?"(.*?)"', content_str)
        tags_match = _re.search(r'hashtags.*?\[(.*?)\]', content_str)

        tab_wx, tab_video, tab_xhs = st.tabs(["📱 朋友圈/公众号", "🎬 视频脚本", "📕 小红书"])
        with tab_wx:
            if wx_match:
                wx_text = wx_match.group(1).replace('\\n', '\n')
                st.text_area(t("朋友圈文案","WeChat Post"), wx_text, height=200, key="wx_copy")
                st.caption(t("👆 选中文字 Ctrl+C 复制 → 微信 Ctrl+V 粘贴","Copy above → Paste to WeChat"))
        with tab_video:
            if video_match:
                st.text_area(t("视频脚本","Video Script"), video_match.group(1).replace('\\n', '\n'), height=200, key="vid_copy")
        with tab_xhs:
            if xhs_match:
                st.markdown(f"**{t('标题','Title')}**: {xhs_match.group(1)}")
                st.text_area(t("正文","Body"), xhs_match.group(2).replace('\\n', '\n'), height=150, key="xhs_copy")
        if tip_match:
            st.info(f"💡 {t('养生日签','Daily Tip')}: {tip_match.group(1)}")
        if tags_match:
            st.caption(f"{t('标签','Tags')}: {tags_match.group(1)}")
    else:
        st.warning(t("今日内容尚未生成，点击按钮生成","Today's content not yet generated"))
        if st.button(t("🎬 生成今日推广内容","🎬 Generate Today's Content"), use_container_width=True):
            with st.spinner(t("生成中...","Generating...")):
                import subprocess, sys as _sys
                subprocess.run([_sys.executable, "bots/auto_pilot.py", "--mode", "today"], cwd=str(Path(__file__).parent.parent))
                st.rerun()

    st.divider()
    st.markdown(f"## 📊 {t('数据统计','Statistics')}")

    # 加载数据
    bookings_file = Path(__file__).parent.parent / "output" / "bookings.jsonl"
    orders_file = Path(__file__).parent.parent / "output" / "orders.jsonl"
    leads_file = Path(__file__).parent.parent / "output" / "leads.jsonl"

    def count_lines(path):
        try: return sum(1 for _ in open(path, encoding='utf-8'))
        except Exception: return 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric(t("📅 预约","Bookings"), count_lines(bookings_file))
    c2.metric(t("🛒 订单","Orders"), count_lines(orders_file))
    c3.metric(t("📧 线索","Leads"), count_lines(leads_file))
    c4.metric(t("💬 问诊","Consults"), len(st.session_state.messages)//2)

    st.divider()

    # 体质分析统计
    st.markdown(f"### {t('📋 体质分布','Constitution Distribution')}")
    cq1,cq2,cq3 = st.columns(3)
    cq1.markdown("**平和质**: 15%")
    cq1.progress(15)
    cq2.markdown("**阴虚质**: 22%")
    cq2.progress(22)
    cq3.markdown("**阳虚质**: 18%")
    cq3.progress(18)
    cq1.markdown("**气虚质**: 20%")
    cq1.progress(20)
    cq2.markdown("**气郁质**: 12%")
    cq2.progress(12)
    cq3.markdown("**痰湿质**: 13%")
    cq3.progress(13)

    st.divider()

    # 最近订单
    st.markdown(f"### {t('🛒 最近订单','Recent Orders')}")
    try:
        orders = []
        if orders_file.exists():
            with open(orders_file, encoding='utf-8') as f:
                for line in f:
                    try: orders.append(json.loads(line))
                    except Exception: pass
        if orders:
            for o in orders[-5:]:
                items = o.get('items',{})
                item_str = ', '.join([f"{k}x{v}" for k,v in items.items()])
                st.markdown(f"**{o.get('name','?')}** | {o.get('phone','?')} | {item_str} | {o.get('time','?')}")
        else:
            st.caption(t("暂无订单","No orders yet"))
    except Exception: pass

    st.divider()
    st.markdown(f"### {t('📈 流量来源','Traffic Sources')}")
    c1,c2,c3 = st.columns(3)
    c1.metric(t("微信","WeChat"), "60%")
    c2.metric(t("直接访问","Direct"), "25%")
    c3.metric(t("分享链接","Referral"), "15%")

# ── 页脚 ──────────────────────────────────────────────────

st.markdown(f"""
<div class="footer">
    <p>🌿 {CLINIC_INFO['name']} · {CLINIC_INFO['name_en']}</p>
    <p>{CLINIC_INFO['slogan']} | {CLINIC_INFO['slogan_en']}</p>
    <p>📞 {CLINIC_INFO['phone']} | 📧 {CLINIC_INFO['email']}</p>
    <p style="margin-top:1rem;font-size:0.75rem;">
        ⚠️ {t('本网站 AI 问诊仅供健康教育参考，不构成医疗建议。请咨询 AHPRA 注册中医师。','AI consultation is for educational purposes only. Not medical advice. Consult an AHPRA-registered practitioner.')}
    </p>
    <p>© 2026 山东本草堂中医诊所</p>
</div>
""", unsafe_allow_html=True)
