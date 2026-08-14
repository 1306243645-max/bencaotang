"""Partner program page of BenCao Tang TCM Clinic."""

import streamlit as st

from web.components.constants import t


def render():
    """Render the partners page."""
    st.markdown(f"## 🤝 {t('全球合伙人计划','Global Partner Program')}")
    st.divider()

    st.markdown(f"""
    <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,rgba(201,169,110,0.1),rgba(201,169,110,0.05));border-radius:12px;margin-bottom:2rem;">
        <h2 style="color:var(--ink-dark);font-weight:300;">{t('共创中医全球化事业','Co-create TCM Globalization')}</h2>
        <p style="color:var(--ink-light);">{t('零成本加入，共享全球中医红利','Zero cost to join, share global TCM dividends')}</p>
    </div>
    """, unsafe_allow_html=True)

    partner_types = st.columns(3)
    with partner_types[0]:
        st.markdown(f"### 🌍 {t('海外合伙人','Overseas Partner')}")
        st.markdown(t(
            "**适合**：海外华人、留学生、中医爱好者\n\n"
            "**做什么**：\n- 推广妙手堂AI问诊\n- 组织当地中医活动\n- 分销养生产品\n\n"
            "**收益**：\n- 产品分销佣金 20-30%\n- 课程推广佣金 30%\n- 问诊推荐佣金 15%",
            "**For**: Overseas Chinese, Students\n\n"
            "**Do**: Promote AI TCM, Local events, Product distribution\n\n"
            "**Earn**: 20-30% product commission, 30% course, 15% consultation"
        ))
    with partner_types[1]:
        st.markdown(f"### 🏥 {t('中医师合伙人','Practitioner Partner')}")
        st.markdown(t(
            "**适合**：注册中医师、针灸师\n\n"
            "**做什么**：\n- 提供远程问诊服务\n- 录制专业课程\n- 参与知识库建设\n\n"
            "**收益**：\n- 问诊收入 70%\n- 课程销售分成 50%\n- 平台流量扶持",
            "**For**: Licensed TCM practitioners\n\n"
            "**Do**: Tele-consultation, Courses, Knowledge base\n\n"
            "**Earn**: 70% consult fee, 50% course, traffic support"
        ))
    with partner_types[2]:
        st.markdown(f"### 📱 {t('内容合伙人','Content Partner')}")
        st.markdown(t(
            "**适合**：自媒体博主、视频创作者\n\n"
            "**做什么**：\n- 制作中医科普内容\n- 运营社交媒体账号\n- 直播推广产品\n\n"
            "**收益**：\n- 内容流量变现 50%\n- 带货佣金 25%\n- 平台流量扶持",
            "**For**: Content creators, bloggers\n\n"
            "**Do**: TCM content, Social media, Live streaming\n\n"
            "**Earn**: 50% content revenue, 25% affiliate, traffic boost"
        ))

    st.divider()
    st.markdown(f"### 📝 {t('加入流程','How to Join')}")
    join_cols = st.columns(4)
    for i, (step, desc) in enumerate([
        ("1️⃣ 提交申请", "填写合伙人申请表"),
        ("2️⃣ 资质审核", "1-3个工作日反馈"),
        ("3️⃣ 签署协议", "电子合同在线签署"),
        ("4️⃣ 开始合作", "开通后台+培训+推广"),
    ]):
        with join_cols[i]:
            st.markdown(f"**{step}**\n\n{desc}")

    st.info(f"📧 {t('合伙人申请邮箱','Partner Application')}: 83497212@qq.com  |  📞 18254191315")
