"""本草堂 · AI问诊小程序页面

独立页面，适合微信内置浏览器和手机访问
访问: https://eleven-trains-kiss.loca.lt/consult_app
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

st.set_page_config(
    page_title="本草堂 · AI智能问诊",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 加载主应用
from agents.base import BaseAgent, Tool
from web.components.constants import TCM_TOOLS, SYSTEM_ZH

st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #E8F5E9, #FAFBFB) !important; }
    header { display: none !important; }
    footer { display: none !important; }
    .consult-header { text-align:center; padding:1.5rem 1rem; }
    .consult-header h1 { color:#2B7A4B; font-size:1.8rem; margin:0; }
    .consult-header p { color:#636E72; margin:0.3rem 0; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="consult-header">
    <h1>🌿 本草堂 · AI 智能问诊</h1>
    <p>描述症状，即刻辨证施治</p>
</div>
""", unsafe_allow_html=True)

# Init agent
if "agent" not in st.session_state:
    agent = BaseAgent(system=SYSTEM_ZH, max_tokens=4096, max_tool_rounds=5)
    for t in TCM_TOOLS: agent.add_tool(t)
    st.session_state.agent = agent

if "msgs" not in st.session_state:
    st.session_state.msgs = []

# Quick templates
if not st.session_state.msgs:
    templates = [
        "失眠睡不着怎么办？",
        "饭后腹胀乏力怎么调理？",
        "手脚冰凉是什么体质？",
        "月经痛怎么缓解？",
        "最近总是疲劳没精神",
    ]
    st.caption("💡 快速提问：")
    cols = st.columns(len(templates))
    for i, tpl in enumerate(templates):
        with cols[i]:
            if st.button(tpl, key=f"tpl_{i}", use_container_width=True):
                st.session_state.msgs.append({"role":"user","content":tpl})
                st.rerun()

# Chat
for msg in st.session_state.msgs:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("描述你的症状..."):
    st.session_state.msgs.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("辨证分析中..."):
            resp = st.session_state.agent.chat(prompt)
            st.markdown(resp.content)
    st.session_state.msgs.append({"role":"assistant","content":resp.content})

# Footer
st.divider()
st.caption("⚠️ 本内容仅供健康教育参考，不替代医生诊断 | 本草堂中医诊所 | 18254191315")
