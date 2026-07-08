"""Expert team page of BenCao Tang TCM Clinic."""

import streamlit as st

from web.components.constants import t


def render():
    """Render the experts page."""
    st.markdown(f"## 👨‍⚕️ {t('名医团队','Expert Team')}")
    st.divider()

    st.markdown(f"""
    <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,rgba(155,142,196,0.08),rgba(181,168,212,0.05));border-radius:12px;margin-bottom:2rem;">
        <h2 style="color:var(--ink-dark);font-weight:300;">{t('三代传承 · 名医荟萃','Three Generations · Expert Network')}</h2>
        <p style="color:var(--ink-light);">{t('本草堂汇聚山东及全国著名中医专家，为您提供专业中医健康服务','Expert TCM practitioners providing professional health services')}</p>
    </div>
    """, unsafe_allow_html=True)

    experts = [
        {"name": t("张树淮 先生","Mr. Zhang Shuhuai"), "title": t("金锁玉关风水第三代传承人","Jin Suo Yu Guan 3rd Gen Inheritor"), "field": t("风水堪舆 · 八字命理","Feng Shui · Ba Zi"), "desc": t("金锁玉关风水学正宗传承人，张秩也老师祖父。","Authentic inheritor of Jin Suo Yu Guan Feng Shui.")},
        {"name": t("张秩也 老师","Mr. Zhang Zhiye"), "title": t("金锁玉关风水讲师","Jin Suo Yu Guan Lecturer"), "field": t("风水教学 · 实战案例","Feng Shui Teaching"), "desc": t("24课完整体系，数百实战案例。","24-course system, hundreds of real cases.")},
        {"name": t("毛小妹 老师","Ms. Mao Xiaomei"), "title": t("五运六气研究专家","Wu Yun Liu Qi Expert"), "field": t("五运六气 · 人体气象站","5 Movements 6 Qi"), "desc": t("创立毛氏运气医学体系，人体气象站理论创始人。","Founder of Mao's Yun Qi Medicine system.")},
        {"name": t("本草堂中医团队","BenCao Tang Team"), "title": t("AI问诊知识库专家组","AI Knowledge Expert Panel"), "field": t("中医学 · AI融合","TCM + AI"), "desc": t("18个知识库，涵盖中医全科。","18 knowledge bases, full TCM coverage.")},
    ]

    for exp in experts:
        with st.expander(f"👨‍⚕️ {exp['name']} — {exp['title']}", expanded=False):
            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown(f"**{t('专长','Field')}**\n\n{exp['field']}")
            with c2:
                st.markdown(exp['desc'])

    st.divider()
    st.markdown(f"### 🏥 {t('合作机构','Partner Institutions')}")
    inst_cols = st.columns(3)
    with inst_cols[0]:
        st.markdown(t("山东中医药大学附属\n山东省中医院","Shandong TCM University"))
    with inst_cols[1]:
        st.markdown(t("中国中医科学院\n中医药信息研究所","China Academy of TCM"))
    with inst_cols[2]:
        st.markdown(t("世界中医药学会联合会\n中医适宜技术委员会","WFCMS"))
