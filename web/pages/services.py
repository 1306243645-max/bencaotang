"""Services page of BenCao Tang TCM Clinic."""

import streamlit as st

from web.components.constants import t


def render():
    """Render the services page."""
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
