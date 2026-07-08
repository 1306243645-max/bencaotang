"""Wellness shop, cart, and orders page of BenCao Tang TCM Clinic."""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter

import streamlit as st

from web.components.constants import t
from web.components.clinic_info import CLINIC_INFO


def render():
    """Render the shop page."""
    st.markdown(f"## 🛒 {t('养生食品商城','Wellness Shop')}")
    st.caption(t("本草堂精选 · 药食同源 · 澳洲配送","BenCao Tang精选 · Food-as-Medicine · AU Delivery"))
    st.divider()

    products = [
        {"name": "菊花枸杞茶包", "price": "$12", "desc": "清肝明目，10包装", "tag": "🔥 热销", "img": "🍵"},
        {"name": "玫瑰红枣养颜茶", "price": "$15", "desc": "疏肝养血，10包装", "tag": "💝 女性必备", "img": "🌹"},
        {"name": "四神汤料包", "price": "$12", "desc": "健脾祛湿，4人份", "tag": "👨‍👩‍👧‍👦 全家适用", "img": "🍲"},
        {"name": "秋梨膏", "price": "$25", "desc": "润肺止咳，250g/瓶", "tag": "🍂 秋季必囤", "img": "🍯"},
        {"name": "黑芝麻核桃粉", "price": "$20", "desc": "补肾乌发，300g/罐", "tag": "💪 男士推荐", "img": "🥜"},
        {"name": "阿胶糕", "price": "$35", "desc": "补血养颜，250g/盒", "tag": "👸 口碑爆款", "img": "🍬"},
        {"name": "安神助眠泡脚包", "price": "$15", "desc": "宁心安神，5次量", "tag": "😴 失眠救星", "img": "🦶"},
        {"name": "艾叶生姜泡脚包", "price": "$10", "desc": "温经散寒，7次量", "tag": "❄️ 冬季必备", "img": "🔥"},
        {"name": "陈皮生姜暖胃茶", "price": "$10", "desc": "温中散寒，10包装", "tag": "👍 口碑好", "img": "🫚"},
        {"name": "花旗参石斛汤料", "price": "$25", "desc": "益气养阴，4人份", "tag": "⭐ 高端滋补", "img": "💎"},
        {"name": "八珍糕", "price": "$18", "desc": "健脾养胃，12块/盒", "tag": "👶 老少皆宜", "img": "🍰"},
        {"name": "桑葚膏", "price": "$22", "desc": "滋阴补血，250g/瓶", "tag": "💆 养发", "img": "🫐"},
    ]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1.2rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:1rem;text-align:center;">
                <div style="font-size:3rem;">{p['img']}</div>
                <span style="background:#fef3c7;color:#92400e;padding:2px 8px;border-radius:1rem;font-size:0.75rem;">{p['tag']}</span>
                <h4 style="margin:0.5rem 0;">{p['name']}</h4>
                <p style="color:#6b7280;font-size:0.85rem;">{p['desc']}</p>
                <p style="font-size:1.3rem;font-weight:700;color:#2d6a4f;">{p['price']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("🛒 加入购物车","🛒 Add to Cart"), key=f"cartbtn_{i}", use_container_width=True):
                st.session_state.cart.append(p["name"])
                st.toast(f"✅ {p['name']}")

    # 购物车
    st.divider()
    st.markdown(f"### 🛒 {t('购物车','Shopping Cart')} ({len(st.session_state.cart)})")
    if st.session_state.cart:
        cart_items = Counter(st.session_state.cart)
        for item, qty in cart_items.items():
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"**{item}** x{qty}")
            if c2.button(t("删除","Remove"), key=f"rm_{item}"):
                st.session_state.cart.remove(item)
                st.rerun()
        if st.button(t("🗑️ 清空购物车","🗑️ Clear Cart"), use_container_width=True):
            st.session_state.cart = []
            st.rerun()
        # 下单表单
        st.markdown("---")
        st.markdown(f"### 📝 {t('提交订单','Submit Order')}")
        order_name = st.text_input(t("姓名","Name"), key="order_name")
        order_phone = st.text_input(t("电话","Phone"), key="order_phone")
        order_addr = st.text_area(t("收货地址","Delivery Address"), key="order_addr")
        if st.button(t("✅ 确认下单","✅ Place Order"), use_container_width=True, type="primary"):
            if order_name and order_phone:
                order = {
                    "name": order_name, "phone": order_phone, "address": order_addr,
                    "items": dict(cart_items), "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                st.session_state.orders.append(order)
                # 保存到文件
                order_file = Path(__file__).parent.parent.parent / "output" / "orders.jsonl"
                order_file.parent.mkdir(exist_ok=True)
                with open(order_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(order, ensure_ascii=False) + "\n")
                st.session_state.cart = []
                st.success(t("✅ 订单已提交！我们将尽快联系您确认。","✅ Order submitted! We'll contact you shortly."))
                st.balloons()
            else:
                st.error(t("请填写姓名和电话。","Please fill in name and phone."))
    else:
        st.caption(t("购物车空空，去逛逛吧~","Your cart is empty."))

    # 支付方式
    st.divider()
    st.markdown(f"### 💰 {t('支付方式','Payment')}")
    pay_col1, pay_col2 = st.columns(2)
    with pay_col1:
        st.markdown(f"**{t('微信支付','WeChat Pay')}**")
        try:
            import qrcode, io, base64 as b64
            pay_qr = qrcode.make("wxp://f2f0x7I7K7jMlylC_lhQWtbMfYsBntF1nXWe")
            buf = io.BytesIO()
            pay_qr.save(buf, format='PNG')
            st.image(buf, width=160, caption=t("扫一扫付款","Scan to Pay"))
        except Exception:
            st.info(t("微信支付二维码","WeChat Pay QR"))
    with pay_col2:
        st.markdown(f"**{t('支付宝','Alipay')}**")
        try:
            ali_qr = qrcode.make("https://qr.alipay.com/fkx18545vbw4lmq8qlnxe66")
            buf2 = io.BytesIO()
            ali_qr.save(buf2, format='PNG')
            st.image(buf2, width=160, caption=t("扫一扫付款","Scan to Pay"))
        except Exception:
            st.info(t("支付宝二维码","Alipay QR"))
    st.caption(t("💡 付款后截图发给微信 {wechat} 确认订单","💡 Send payment screenshot to WeChat {wechat}").format(wechat=CLINIC_INFO['wechat']))

    st.divider()
    st.markdown(f"### {t('📦 其他购买方式','Other Ways to Order')}")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**1️⃣ {t('微信下单','WeChat Order')}**\n\n{t('添加微信直接下单，转账后发地址当天发货','Add WeChat to order')}: {CLINIC_INFO['wechat']}")
    c2.markdown(f"**2️⃣ {t('电话订购','Phone Order')}**\n\n{t('拨打','Call')}: {CLINIC_INFO['phone']}")
    c3.markdown(f"**3️⃣ {t('到店选购','Visit Us')}**\n\n{CLINIC_INFO['address']}")
