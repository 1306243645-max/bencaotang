"""Global sidebar content for MiaoShou Tang web app."""

import io
import streamlit as st
import qrcode
import base64 as b64

from web.components.clinic_info import CLINIC_INFO
from web.components.constants import t, TCM_TOOLS, SYSTEM_ZH, SYSTEM_EN


def switch_lang(lang):
    """Switch language and recreate the agent."""
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        system = SYSTEM_ZH if lang == "zh" else SYSTEM_EN
        from agents.base import BaseAgent
        agent = BaseAgent(system=system, max_tokens=8192, max_tool_rounds=8)
        for tool in TCM_TOOLS:
            agent.add_tool(tool)
        st.session_state.agent = agent
        st.rerun()


SITE_URL = "https://妙手堂.icu"


def _make_wx_qr():
    """Generate a simple WeChat QR code image (base64)."""
    qr = qrcode.make(SITE_URL)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    return b64.b64encode(buf.getvalue()).decode()


def _make_styled_qr():
    """Generate a styled QR code for the clinic URL (base64), with fallback."""
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=4,
        )
        qr.add_data(SITE_URL)
        qr.make(fit=True)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="#2d6a4f",
            back_color="white",
        )
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        return b64.b64encode(buf.getvalue()).decode()
    except Exception:
        qr_img = qrcode.make(SITE_URL)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        return b64.b64encode(buf.getvalue()).decode()


def render_sidebar():
    """Render the global sidebar content."""
    L = st.session_state.lang

    st.markdown("## 🏥 妙手堂")
    st.caption(f"🌍 {CLINIC_INFO['domain']}")
    st.divider()

    # ── 二维码 ──
    st.markdown(f"#### 📱 {t('扫码访问妙手堂', 'Scan for MiaoShou Tang')}")
    qb = _make_wx_qr()
    st.markdown(
        f'<div style="text-align:center"><img src="data:image/png;base64,{qb}" width="140"></div>',
        unsafe_allow_html=True,
    )
    st.caption(f"📸 {t('微信扫码直接访问', 'Scan to visit')}")

    st.caption(t("三代传承 · 正宗中医", "Heritage TCM · Since 1980s"))
    st.divider()

    # ── 语言切换 ──
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("🇨🇳 中文", use_container_width=True,
                     type="primary" if L == "zh" else "secondary"):
            switch_lang("zh")
    with col_r:
        if st.button("🇦🇺 EN", use_container_width=True,
                     type="primary" if L == "en" else "secondary"):
            switch_lang("en")
    st.divider()

    # ── 联系方式 ──
    st.markdown(f"**📞** {CLINIC_INFO['phone']}")
    st.markdown(f"**📧** {CLINIC_INFO['email']}")
    st.markdown(f"**💬** 微信：{CLINIC_INFO['wechat']}")
    st.divider()

    # ── 社交媒体矩阵 ──
    st.markdown(f"#### 🌐 {t('社交媒体', 'Social Media')}")
    social_html = f"""
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;justify-content:center;">
    <a href="https://xiaohongshu.com/user/profile/{CLINIC_INFO['xiaohongshu']}" target="_blank" style="background:#FE2C55;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📕 小红书</a>
    <a href="https://youtube.com/@{CLINIC_INFO['youtube']}" target="_blank" style="background:#FF0000;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📺 YouTube</a>
    <a href="https://reddit.com/user/{CLINIC_INFO['reddit']}" target="_blank" style="background:#FF4500;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🧵 Reddit</a>
    <a href="https://tiktok.com/@bencaotang" target="_blank" style="background:#000;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🎬 TikTok</a>
    <a href="https://facebook.com/MiaoShouTang" target="_blank" style="background:#1877F2;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📘 FB</a>
    <a href="https://instagram.com/miaoshoutang" target="_blank" style="background:#E4405F;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📷 IG</a>
    </div>
    """
    st.markdown(social_html, unsafe_allow_html=True)
    st.divider()

    # ── 精美二维码 ──
    st.markdown(f"#### 📱 {t('扫码打开妙手堂', 'Scan for MiaoShou Tang')}")
    qr_b64_img = _make_styled_qr()
    st.markdown(
        f'<div style="text-align:center;background:white;padding:12px;border-radius:12px;display:inline-block;">'
        f'<img src="data:image/png;base64,{qr_b64_img}" width="180"></div>',
        unsafe_allow_html=True,
    )
    st.caption(f"🔗 {SITE_URL}")
    st.caption(t("💡 扫码不成功？截图→微信扫一扫→相册",
                 "💡 Can't scan? Screenshot → WeChat → Album"))

    # ── 推荐有礼 ──
    st.divider()
    st.markdown(f"#### 🎁 {t('推荐有礼', 'Referral Program')}")
    if st.session_state.ref:
        st.success(t(f"🎉 来自推荐: {st.session_state.ref}",
                     "🎉 Referred by: " + st.session_state.ref))
    st.metric(t("今日分享", "Shares Today"), st.session_state.shares)
    st.caption(t("每推荐1位好友 → 双方各得免费体质茶1份",
                 "Refer a friend → Both get free tea"))
    st.divider()
    st.caption("© 2026 山东妙手堂中医诊所")
