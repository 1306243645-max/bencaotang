"""About page of BenCao Tang TCM Clinic."""

import streamlit as st

from web.components.constants import t
from web.components.clinic_info import CLINIC_INFO


def render():
    """Render the about page."""
    st.markdown(f"## 📖 {t('关于妙手堂','About BenCao Tang')}")
    st.divider()

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown(f"""
        ### {t('我们的故事','Our Story')}

        {t(
        '山东妙手堂中医诊所，源自齐鲁大地，三代中医世家传承。创始人张老先生上世纪 80 年代在山东济南创立妙手堂，以"本草济世、仁心济世"为堂训，服务一方百姓。',
        'Shandong BenCao Tang TCM Clinic traces its roots to Jinan, Shandong Province, where the founding family has practiced Chinese medicine for three generations since the 1980s.'
        )}

        {t(
        '第二代传人在家传基础上，融汇现代医学理念，将妙手堂发展为集针灸、中药、推拿、食疗为一体的综合性中医诊所。',
        'The second generation integrated modern medical knowledge with traditional wisdom, expanding the clinic into a comprehensive TCM practice covering acupuncture, herbal medicine, tuina massage, and dietary therapy.'
        )}

        {t(
        '如今，第三代传人将妙手堂带到澳大利亚悉尼，致力于为澳洲华人社区及本地居民提供正宗、专业、温暖的中医健康服务。我们结合 AI 技术，让传统中医更加便捷、精准。',
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
