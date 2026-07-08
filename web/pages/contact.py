"""Booking and contact page of BenCao Tang TCM Clinic."""

import json
from pathlib import Path
from datetime import datetime
import streamlit as st

from web.components.constants import t
from web.components.clinic_info import CLINIC_INFO


def render():
    """Render the contact / booking page."""
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
                booking_file = Path(__file__).parent.parent.parent / "output" / "bookings.jsonl"
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
