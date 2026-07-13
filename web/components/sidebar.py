"""Global sidebar content for BenCao Tang web app."""

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


def _make_wx_qr():
    """Generate a simple WeChat QR code image (base64)."""
    qr = qrcode.make('https://eleven-trains-kiss.loca.lt')
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    return b64.b64encode(buf.getvalue()).decode()


def _make_styled_qr():
    """Generate a styled QR code for the clinic URL (base64), with fallback."""
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer

    mst_url = "https://eleven-trains-kiss.loca.lt"
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=4,
        )
        qr.add_data(mst_url)
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
        qr_img = qrcode.make(mst_url)
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        return b64.b64encode(buf.getvalue()).decode()


def render_sidebar():
    """Render the global sidebar content."""
    L = st.session_state.lang

    st.markdown("## 本草堂")
    # 萌宠已移除
    # 访问地址提示
    st.caption("🌍 公网: 本草堂.icu")
    st.divider()
    st.markdown("#### 📱 AI问诊小程序")
    qb = _make_wx_qr()
    st.markdown(
        f'<div style="text-align:center"><img src="data:image/png;base64,{qb}" width="140"></div>',
        unsafe_allow_html=True,
    )
    st.caption("📸 微信扫码直接问诊")

    st.caption(t("三代传承 · 正宗中医", "Heritage TCM · Since 1980s"))
    st.divider()
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
    st.markdown(f"**📞** {CLINIC_INFO['phone']}")
    st.markdown(f"**📧** {CLINIC_INFO['email']}")
    st.markdown(f"**💬** 微信：{CLINIC_INFO['wechat']}")
    st.divider()
    # ── 社交媒体矩阵 ──
    st.markdown("#### 🌐 社交媒体")
    social_html = """
    <div style="display:flex;flex-wrap:wrap;gap:0.4rem;justify-content:center;">
    <a href="https://weibo.com/本草堂" target="_blank" style="background:#E6162D;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🧣 微博</a>
    <a href="https://xiaohongshu.com/本草堂" target="_blank" style="background:#FE2C55;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📕 小红书</a>
    <a href="https://douyin.com/本草堂" target="_blank" style="background:#111;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🎵 抖音</a>
    <a href="https://facebook.com/BenCaoTang" target="_blank" style="background:#1877F2;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📘 FB</a>
    <a href="https://instagram.com/bencaotang_tcm" target="_blank" style="background:#E4405F;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">📷 IG</a>
    <a href="https://tiktok.com/@bencaotang" target="_blank" style="background:#000;color:white;padding:4px 10px;border-radius:12px;text-decoration:none;font-size:0.75rem;">🎬 TikTok</a>
    </div>
    """
    st.markdown(social_html, unsafe_allow_html=True)
    st.divider()
    # ── 本草堂二维码（高容错+白边）──
    st.markdown(f"#### 📱 {t('扫码打开本草堂', 'Scan for BenCao Tang')}")
    qr_b64_img = _make_styled_qr()
    st.markdown(
        f'<div style="text-align:center;background:white;padding:12px;border-radius:12px;display:inline-block;">'
        f'<img src="data:image/png;base64,{qr_b64_img}" width="180"></div>',
        unsafe_allow_html=True,
    )

    st.caption(f"📱 {t('微信扫码打开本草堂官网', 'Scan with WeChat to open')}")
    st.caption(f"🔗 {t('公网链接', 'Public URL')}: 本草堂.icu")
    st.caption(t("💡 扫码不成功？试试截图→微信扫一扫→相册",
                 "💡 Can't scan? Screenshot → WeChat → Album"))

    # 推荐追踪
    st.divider()
    st.markdown(f"#### 🎯 {t('推荐有礼', 'Referral Program')}")
    if st.session_state.ref:
        st.success(t(f"🎉 来自推荐: {st.session_state.ref}",
                     "🎉 Referred by: " + st.session_state.ref))
    st.metric(t("今日分享", "Shares Today"), st.session_state.shares)
    st.caption(t("每推荐1位好友 → 双方各得免费体质茶1份",
                 "Refer a friend → Both get free tea"))
    st.divider()
    st.caption("© 2026 山东本草堂中医诊所")
