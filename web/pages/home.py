"""Home page of MiaoShou Tang TCM Clinic."""

import streamlit as st

from web.components.constants import t, TCM_TOOLS, SYSTEM_EN


def render():
    """Render the home page."""
    st.markdown(f"""
    <div style="text-align:center;padding:3rem 2rem;background:linear-gradient(135deg,#2C1810,#3C2820,#2C1810);border-radius:16px;margin-bottom:2rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:20px;right:30px;font-size:5rem;opacity:0.1;">🐱</div>
        <div style="font-size:4rem;margin-bottom:0.5rem;">🐱</div>
        <h1 style="color:#FFD700;font-size:2.2rem;font-weight:700;margin:0.5rem 0;">AI 智能中医问诊</h1>
        <p style="color:#E0D5C0;font-size:1.1rem;">18个知识库 · 五运六气 · 面诊 · 舌诊 · 茶饮 · 偏方</p>
        <p style="color:#B5A8D4;font-size:0.9rem;">描述症状，小白即刻辨证施治</p>
    </div>
    """, unsafe_allow_html=True)

    # 装饰分隔
    st.markdown("""
    <div style="text-align:center;padding:1rem 0;">
        <span style="color:#D9D2E6;font-size:1.2rem;letter-spacing:0.3em;">◆ ◇ ◆</span>
    </div>
    """, unsafe_allow_html=True)

    # 访问方式
    st.info(f"🔗 {t('妙手堂访问地址','Find us at')}: 妙手堂.icu | {t('微信搜','WeChat')}: 妙手堂 | 📞 18254191315")

    st.markdown(f"### {t('本堂特色','Our Heritage')}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="service-card"><h4>🌿 ' + t('三代中医传承','Heritage TCM') + '</h4><p>' + t('山东中医世家，三代人专注中医诊疗，将正宗的中医智慧带到澳大利亚。','Three generations of TCM practitioners bringing authentic Chinese medicine to Australia.') + '</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="service-card"><h4>🤖 ' + t('AI + 中医','AI + TCM') + '</h4><p>' + t('自研 AI 问诊系统，24/7 在线健康咨询，智能体质辨识，让中医触手可及。','AI-powered health advisor available 24/7 for TCM consultation and constitution analysis.') + '</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="service-card"><h4>🇦🇺 ' + t('澳洲合规','AU Registered') + '</h4><p>' + t('AHPRA 注册中医师执业，TGA 合规药材，Medibank/Bupa 可报销。','AHPRA-registered practitioners, TGA-compliant herbs, private health fund rebates available.') + '</p></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### {t('📊 快速开始','📊 Quick Start')}")

    # AI问诊突出入口
    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem;margin:1rem 0;background:linear-gradient(135deg,#EDE8F5,#F5F2FA);border-radius:12px;border:2px solid #B5A8D4;">
        <div style="font-size:2.5rem;">🐱</div>
        <h3 style="color:#3C3C3C;margin:0.3rem 0;">{t('AI 智能问诊','AI Smart Consultation')}</h3>
        <p style="color:#8C8C8C;">{t('18个知识库 · 五运六气·面诊·舌诊·茶饮·偏方·风水','18 KB · 5D Analysis')}</p>
    </div>
    """, unsafe_allow_html=True)

    cq1, cq2, cq3 = st.columns(3)
    with cq1:
        if st.button(t("💬 开始AI问诊","💬 Start AI Consult"), use_container_width=True, type="primary"):
            st.session_state.page = "consult"
            st.rerun()
    with cq2:
        if st.button(t("📋 体质自测","📋 Constitution Test"), use_container_width=True):
            st.session_state.page = "consult"
            st.rerun()
    with cq3:
        if st.button(t("🌍 Overseas","🌍 English"), use_container_width=True):
            st.session_state.lang = "en"
            from agents.base import BaseAgent
            st.session_state.agent = BaseAgent(system=SYSTEM_EN, max_tokens=8192, max_tool_rounds=8)
            for t_ in TCM_TOOLS:
                st.session_state.agent.add_tool(t_)
            st.session_state.page = "consult"
            st.rerun()
