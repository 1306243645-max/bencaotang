"""Culture / Global Outreach page of BenCao Tang TCM Clinic."""

import streamlit as st

from web.components.constants import t


def render():
    """Render the culture page."""
    st.markdown(f"## 🏯 {t('中医文化出海','TCM Culture Global')}")
    st.divider()

    st.markdown(f"""
    <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,rgba(155,142,196,0.08),rgba(181,168,212,0.05));border-radius:12px;margin-bottom:2rem;">
        <h2 style="color:var(--ink-dark);font-weight:300;">{t('以文化为舟，让中医走向世界','Culture as vessel, TCM goes global')}</h2>
        <p style="color:var(--ink-light);">{t('本草堂 · 全球中医文化传播平台','BenCao Tang · Global TCM Culture Platform')}</p>
    </div>
    """, unsafe_allow_html=True)

    pillars = st.columns(3)
    with pillars[0]:
        st.markdown(f"### 📚 {t('文化传承','Heritage')}")
        st.markdown(t(
            "- 《黄帝内经》英译版\n- 五运六气全球教学\n- 二十四节气养生体系\n- 中医经典数字化\n- 非遗中医技艺保护",
            "- Huangdi Neijing English\n- Wu Yun Liu Qi Global\n- 24 Solar Terms Wellness\n- TCM Digital Archive"
        ))
    with pillars[1]:
        st.markdown(f"### 🌏 {t('全球传播','Global Reach')}")
        st.markdown(t(
            "- TikTok/YouTube双语内容\n- 海外中医文化节\n- 国际学术交流\n- 留学生中医社团\n- 海外中医体验中心",
            "- TikTok/YT Bilingual\n- TCM Culture Festival\n- Academic Exchange\n- Student TCM Clubs\n- Experience Centers"
        ))
    with pillars[2]:
        st.markdown(f"### 💼 {t('商业出海','Business')}")
        st.markdown(t(
            "- AI问诊全球服务\n- 跨境养生产品\n- 海外中医培训\n- 企业健康讲座\n- 中医文旅项目",
            "- AI Consultation Global\n- Cross-border Products\n- TCM Training\n- Corporate Wellness\n- TCM Tourism"
        ))

    st.divider()
    st.markdown(f"### 🎯 {t('2026出海计划','2026 Global Plan')}")
    plan_cols = st.columns(4)
    targets = [
        ("Q1", "🇸🇬 新加坡", t("AI问诊上线","AI Launch")),
        ("Q2", "🇦🇪 迪拜", t("文化体验中心","Culture Center")),
        ("Q3", "🇦🇺 悉尼", t("留学生社群","Student Community")),
        ("Q4", "🇬🇧 伦敦", t("中医课程上线","TCM Courses")),
    ]
    for i, (q, country, action) in enumerate(targets):
        with plan_cols[i]:
            st.markdown(f"**{q}** {country}\n\n{action}")
