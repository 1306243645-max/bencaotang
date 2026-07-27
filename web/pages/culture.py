"""Culture / Global Outreach page of MiaoShou Tang TCM Clinic."""

import streamlit as st
from web.components.constants import t
from web.components.clinic_info import CLINIC_INFO


def render():
    L = st.session_state.lang

    st.markdown(f"## 🏯 {t('中医文化出海','TCM Culture Global')}")
    st.markdown(t(
        "以文化为舟，让中医走向世界 | Culture as vessel, TCM goes global",
        "Bridging East and West through Traditional Chinese Medicine"
    ))
    st.divider()

    # ── 出海看板 ──
    st.markdown(f"### 🌊 {t('出海进度看板','Global Progress Board')}")

    platforms = [
        ("📕 小红书", "5275607968", "✅", "国内精准获客"),
        ("🎵 TikTok", "bencaotang", "✅", "海外短视频流量"),
        ("📺 YouTube", CLINIC_INFO.get("youtube", "JIANYUEJIANG"), "✅", "长视频SEO"),
        ("🧵 Reddit", CLINIC_INFO.get("reddit", ""), "✅", "海外中医社区"),
        ("💳 PayPal", CLINIC_INFO.get("paypal", ""), "✅", "海外收款"),
        ("🛒 1688", "代发", "✅", "供应链"),
        ("🌐 官网", CLINIC_INFO.get("domain", "妙手堂.icu"), "✅", "核心枢纽"),
    ]

    for name, handle, status, desc in platforms:
        c1, c2, c3, c4 = st.columns([2, 2, 1, 3])
        with c1: st.markdown(f"**{name}**")
        with c2: st.caption(handle)
        with c3: st.markdown(status)
        with c4: st.caption(desc)

    st.divider()

    # ── 三根支柱 ──
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"### 📚 {t('文化传承','Heritage')}")
        st.markdown(t("""
- 二十四节气养生体系
- 九种体质辨证法
- 五运六气教学
- 《黄帝内经》普及
- 茶饮食疗文化
        """, """
- 24 Solar Terms Wellness
- 9 Constitution Types
- 5 Movements 6 Qi
- Huangdi Neijing
- Tea & Diet Therapy
        """))

    with col2:
        st.markdown(f"### 🌏 {t('全球传播','Global Reach')}")
        st.markdown(t("""
- TikTok 中医科普
- YouTube 英文课程
- Reddit 社区讨论
- 小红书国风内容
- 海外文化体验
        """, """
- TikTok TCM Shorts
- YouTube English Courses
- Reddit TCM Community
- Instagram Wellness
- Global Workshops
        """))

    with col3:
        st.markdown(f"### 💼 {t('商业出海','Business')}")
        st.markdown(t("""
- AI 体质测评
- 跨境茶饮产品
- PayPal 全球收款
- 海外中医培训
- 企业健康讲座
        """, """
- AI Constitution Test
- Cross-border Tea Products
- PayPal Global Payment
- TCM Training Programs
- Corporate Wellness
        """))

    st.divider()

    # ── 内容矩阵 ──
    st.markdown(f"### 🎬 {t('出海内容矩阵','Content Matrix')}")

    content_cols = st.columns(4)
    items = [
        ("🎵", t("短视频","Shorts"), t("TikTok/抖音","TikTok"), t("60秒中医科普\n体质测试引流","60s TCM Tips\nConstitution Quiz")),
        ("📺", t("长视频","Long Form"), t("YouTube"), t("中医课程系列\n姜枣茶教学","TCM Course Series\nHerbal Tea Guide")),
        ("📝", t("图文","Articles"), t("Reddit/小红书","Reddit/XHS"), t("深度科普帖\n社区讨论","Deep Dives\nCommunity Posts")),
        ("📧", t("邮件","Email"), t("Newsletter"), t("节气养生周报\n产品上新","Solar Term Tips\nNew Products")),
    ]
    for i, (icon, title, platform, desc) in enumerate(items):
        with content_cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;border:1px solid #ddd;border-radius:12px;height:180px;">
                <div style="font-size:2rem;">{icon}</div>
                <strong>{title}</strong>
                <p style="font-size:0.8rem;color:#888;">{platform}</p>
                <p style="font-size:0.75rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── 产品出海 ──
    st.markdown(f"### 🛍️ {t('产品出海','Products Going Global')}")

    prod_cols = st.columns(4)
    products = [
        ("🍵", t("体质定制茶","Custom Tea"), "¥68-198/月", t("9种体质\n一人一茶","9 Body Types\nPersonalized")),
        ("🍲", t("食疗汤包","Soup Packs"), "¥88-268", t("四神汤/八珍汤\n药食同源","Authentic TCM\nHerbal Soups")),
        ("📦", t("三伏套装","Sanfu Kit"), "¥298", t("三伏贴+姜枣茶\n冬病夏治","Patches+Tea\nSummer Cure")),
        ("📋", t("体质报告","Report"), "¥9.9", t("AI深度分析\n30页PDF","AI Deep Analysis\n30-page PDF")),
    ]
    for i, (icon, name, price, desc) in enumerate(products):
        with prod_cols[i]:
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;border:1px solid #e0d5c0;border-radius:12px;background:#faf8f4;">
                <div style="font-size:2rem;">{icon}</div>
                <strong>{name}</strong>
                <p style="color:#c0392b;font-weight:bold;">{price}</p>
                <p style="font-size:0.75rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.caption(f"💳 PayPal: {CLINIC_INFO.get('paypal','')} | {t('海外直邮，微信客服','Global Shipping, WeChat Support')}")

    st.divider()

    # ── 海外用户入口 ──
    st.markdown(f"### 🌍 {t('海外用户快速入口','Quick Start for Overseas Users')}")
    qc1, qc2, qc3 = st.columns(3)
    with qc1:
        if st.button(t("🧪 免费测体质","🧪 Free Constitution Test"), use_container_width=True, type="primary"):
            st.session_state.page = "consult"
            st.rerun()
    with qc2:
        st.link_button(t("🎵 TikTok 关注","🎵 Follow TikTok"), "https://tiktok.com/@bencaotang", type="secondary")
        st.caption("") # must be after link_button
        st.markdown(f'<a href="https://tiktok.com/@bencaotang" target="_blank" style="display:inline-block;padding:0.4rem 1rem;background:#000;color:white;border-radius:8px;text-decoration:none;width:100%;text-align:center;">🎬 TikTok</a>', unsafe_allow_html=True)
    with qc3:
        st.link_button(t("📺 YouTube 订阅","📺 YouTube"), f"https://youtube.com/@{CLINIC_INFO.get('youtube','JIANYUEJIANG')}", type="secondary")
        st.markdown(f'<a href="https://youtube.com/@{CLINIC_INFO.get("youtube","JIANYUEJIANG")}" target="_blank" style="display:inline-block;padding:0.4rem 1rem;background:#FF0000;color:white;border-radius:8px;text-decoration:none;width:100%;text-align:center;">📺 YouTube</a>', unsafe_allow_html=True)

    st.divider()

    # ── 文化内容展示 ──
    st.markdown(f"### 🎨 {t('本周出海内容','This Week Content')}")
    content_tabs = st.tabs([
        t("🌞 三伏养生","🌞 Sanfu Wellness"),
        t("🍵 茶道文化","🍵 Tea Culture"),
        t("🧘 八段锦","🧘 Ba Duan Jin"),
    ])

    with content_tabs[0]:
        st.markdown(t("""
        ### 🌞 三伏天养生（Sanfu Wellness）

        2026年三伏：7.15 - 8.23，共40天

        **核心概念**：冬病夏治（Dong Bing Xia Zhi）
        - 三伏贴：大椎穴、肺俞穴、脾俞穴
        - 姜枣茶：生姜3-5片+红枣5颗，早上煮水
        - 艾灸：足三里、关元、涌泉

        **英文传播点**：*"Treat winter diseases in summer — the 40-day golden window of Chinese Medicine"*
        """, """
        ### 🌞 Sanfu Wellness (2026)

        July 15 - Aug 23, 40 days total

        **Core Concept**: Dong Bing Xia Zhi (Winter Disease, Summer Cure)
        - Sanfu Patches: Dazhui (GV14), Feishu (BL13), Pishu (BL20)
        - Ginger-Jujube Tea: 3-5 slices ginger + 5 red dates, morning only
        - Moxibustion: Zusanli (ST36), Guanyuan (CV4), Yongquan (KI1)

        **Key Message**: *"The 40-day golden window of Chinese Medicine"*
        """))

    with content_tabs[1]:
        st.markdown(t("""
        ### 🍵 中国茶道与中医（Tea & TCM）

        **体质对应茶饮**：
        - 气虚 → 黄芪红枣茶
        - 阳虚 → 姜枣茶
        - 阴虚 → 百合银耳羹
        - 痰湿 → 陈皮茯苓茶
        - 湿热 → 菊花金银花茶

        **海外叙事**：*"Not all tea is for everyone — find your constitution, find your tea"*
        """, """
        ### 🍵 Chinese Tea & Body Types

        **Constitution → Tea Pairing**:
        - Qi Deficient → Astragalus + Jujube
        - Yang Deficient → Ginger + Jujube
        - Yin Deficient → Lily Bulb + Tremella
        - Phlegm-Damp → Tangerine Peel + Poria
        - Damp-Heat → Chrysanthemum + Honeysuckle

        *"Find your constitution, find your tea"*
        """))

    with content_tabs[2]:
        st.markdown(t("""
        ### 🧘 八段锦（Ba Duan Jin / Eight Brocades）

        TikTok 播放量超 3 亿次！海外年轻人最爱的中国养生功法。

        **八式名称**：
        1. 双手托天理三焦
        2. 左右开弓似射雕
        3. 调理脾胃须单举
        4. 五劳七伤往后瞧
        5. 摇头摆尾去心火
        6. 两手攀足固肾腰
        7. 攒拳怒目增气力
        8. 背后七颠百病消

        **传播标签**：#BaDuanJin #Qigong #TCM
        """, """
        ### 🧘 Ba Duan Jin (Eight Brocades Qigong)

        300M+ views on TikTok! The most viral Chinese wellness practice.

        **8 Movements**:
        1. Two Hands Hold Up the Heavens
        2. Drawing the Bow to Shoot the Eagle
        3. Separate Heaven and Earth
        4. Wise Owl Gazes Backward
        5. Sway the Head and Shake the Tail
        6. Two Hands Hold the Feet
        7. Clench the Fists and Glare Fiercely
        8. Bouncing on the Toes

        **Hashtags**: #BaDuanJin #Qigong #TCM #ChineseWellness
        """))
