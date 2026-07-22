"""山东妙手堂中医诊所 · MiaoShou Tang TCM Clinic — 官网"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from web.components.constants import (
    t, TCM_TOOLS, SYSTEM_ZH, SYSTEM_EN, NAV_PAGES,
)
from web.components.clinic_info import CLINIC_INFO
from web.components.styles import inject_css
from web.components.sidebar import render_sidebar

# ── 页面配置 ──────────────────────────────────────────────

st.set_page_config(page_title="妙手堂中医诊所", page_icon="🌿", layout="wide")

# ── CSS ───────────────────────────────────────────────────

inject_css()

# ── 初始化 ────────────────────────────────────────────────

if "lang" not in st.session_state:
    st.session_state.lang = "zh"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tool_count" not in st.session_state:
    st.session_state.tool_count = 0
if "bookings" not in st.session_state:
    st.session_state.bookings = []
if "cart" not in st.session_state:
    st.session_state.cart = []
if "orders" not in st.session_state:
    st.session_state.orders = []
if "ref" not in st.session_state:
    st.session_state.ref = st.query_params.get("ref", "")
if "shares" not in st.session_state:
    st.session_state.shares = 0

if "agent" not in st.session_state:
    from agents.base import BaseAgent
    system = SYSTEM_ZH if st.session_state.lang == "zh" else SYSTEM_EN
    agent = BaseAgent(system=system, max_tokens=8192, max_tool_rounds=8)
    for tool_ in TCM_TOOLS:
        agent.add_tool(tool_)
    st.session_state.agent = agent

L = st.session_state.lang

# ── 顶部导航 ─────────────────────────────────────────────

nav_pages = NAV_PAGES
cols_nav = st.columns([0.3] + [1] * len(nav_pages) + [0.3])
for i, (page_id, icon, zh_label, en_label) in enumerate(nav_pages):
    with cols_nav[i + 1]:
        cls = "nav-btn active" if st.session_state.page == page_id else "nav-btn"
        label = t(zh_label, en_label)
        if st.button(f"{icon} {label}", key=f"nav_{page_id}", use_container_width=True):
            st.session_state.page = page_id
            st.rerun()

st.divider()

# ── 侧边栏（全局） ────────────────────────────────────────

with st.sidebar:
    render_sidebar()

# ── 页面路由 ─────────────────────────────────────────────

from web.pages.home import render as render_home
from web.pages.consult import render as render_consult
from web.pages.shop import render as render_shop
from web.pages.culture import render as render_culture
from web.pages.partners import render as render_partners
from web.pages.experts import render as render_experts
from web.pages.contact import render as render_contact
from web.pages.dashboard import render as render_dashboard
from web.pages.about import render as render_about
from web.pages.services import render as render_services
from web.pages.recipes import render as render_recipes

_page_map = {
    "home": render_home,
    "consult": render_consult,
    "shop": render_shop,
    "culture": render_culture,
    "partners": render_partners,
    "experts": render_experts,
    "contact": render_contact,
    "dashboard": render_dashboard,
    "about": render_about,
    "services": render_services,
    "recipes": render_recipes,
}

page = st.session_state.page
if page in _page_map:
    _page_map[page]()
else:
    render_home()

# ── 页脚 ──────────────────────────────────────────────────

st.markdown(f"""
<div class="footer">
    <p>🐼 {CLINIC_INFO['name']} · {CLINIC_INFO['name_en']}</p>
    <p>{CLINIC_INFO['slogan']} | {CLINIC_INFO['slogan_en']}</p>
    <p>📞 {CLINIC_INFO['phone']} | 📧 {CLINIC_INFO['email']}</p>
    <p style="margin-top:1rem;font-size:0.75rem;">
        ⚠️ {t('本网站 AI 问诊仅供健康教育参考，不构成医疗建议。请咨询 AHPRA 注册中医师。','AI consultation is for educational purposes only. Not medical advice. Consult an AHPRA-registered practitioner.')}
    </p>
    <p>© 2026 山东妙手堂中医诊所</p>
</div>
""", unsafe_allow_html=True)
