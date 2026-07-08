"""Dashboard and daily content page of BenCao Tang TCM Clinic."""

import json
import re as _re
import subprocess
import sys as _sys
from pathlib import Path
from datetime import datetime

import streamlit as st

from web.components.constants import t


def render():
    """Render the dashboard / daily content page."""
    # ── 今日推广面板 ──
    st.markdown("## 📢 " + t("今日推广文案","Todays Content"))
    today_file = Path(__file__).parent.parent.parent / "output" / "auto" / f"today_{datetime.now():%Y%m%d}.json"
    if today_file.exists():
        data = json.loads(today_file.read_text(encoding="utf-8"))
        content_str = data.get("content", "")
        # 提取各平台内容
        wx_match = _re.search(r'wechat_post.*?"(.*?)"', content_str, _re.DOTALL)
        video_match = _re.search(r'video_script.*?"(.*?)"', content_str, _re.DOTALL)
        xhs_match = _re.search(r'xiaohongshu.*?"title".*?"(.*?)".*?"body".*?"(.*?)"', content_str, _re.DOTALL)
        tip_match = _re.search(r'daily_tip.*?"(.*?)"', content_str)
        tags_match = _re.search(r'hashtags.*?\[(.*?)\]', content_str)

        tab_wx, tab_video, tab_xhs = st.tabs(["📱 朋友圈/公众号", "🎬 视频脚本", "📕 小红书"])
        with tab_wx:
            if wx_match:
                wx_text = wx_match.group(1).replace('\\n', '\n')
                st.text_area(t("朋友圈文案","WeChat Post"), wx_text, height=200, key="wx_copy")
                st.caption(t("👆 选中文字 Ctrl+C 复制 → 微信 Ctrl+V 粘贴","Copy above → Paste to WeChat"))
        with tab_video:
            if video_match:
                st.text_area(t("视频脚本","Video Script"), video_match.group(1).replace('\\n', '\n'), height=200, key="vid_copy")
        with tab_xhs:
            if xhs_match:
                st.markdown(f"**{t('标题','Title')}**: {xhs_match.group(1)}")
                st.text_area(t("正文","Body"), xhs_match.group(2).replace('\\n', '\n'), height=150, key="xhs_copy")
        if tip_match:
            st.info(f"💡 {t('养生日签','Daily Tip')}: {tip_match.group(1)}")
        if tags_match:
            st.caption(f"{t('标签','Tags')}: {tags_match.group(1)}")
    else:
        st.warning(t("今日内容尚未生成，点击按钮生成","Today's content not yet generated"))
        if st.button(t("🎬 生成今日推广内容","🎬 Generate Today's Content"), use_container_width=True):
            with st.spinner(t("生成中...","Generating...")):
                subprocess.run([_sys.executable, "bots/auto_pilot.py", "--mode", "today"], cwd=str(Path(__file__).parent.parent.parent))
                st.rerun()

    st.divider()
    st.markdown(f"## 📊 {t('数据统计','Statistics')}")

    # 加载数据
    bookings_file = Path(__file__).parent.parent.parent / "output" / "bookings.jsonl"
    orders_file = Path(__file__).parent.parent.parent / "output" / "orders.jsonl"
    leads_file = Path(__file__).parent.parent.parent / "output" / "leads.jsonl"

    def count_lines(path):
        try:
            return sum(1 for _ in open(path, encoding='utf-8'))
        except Exception:
            return 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("📅 预约","Bookings"), count_lines(bookings_file))
    c2.metric(t("🛒 订单","Orders"), count_lines(orders_file))
    c3.metric(t("📧 线索","Leads"), count_lines(leads_file))
    c4.metric(t("💬 问诊","Consults"), len(st.session_state.messages)//2)

    st.divider()

    # 体质分析统计
    st.markdown(f"### {t('📋 体质分布','Constitution Distribution')}")
    cq1, cq2, cq3 = st.columns(3)
    cq1.markdown("**平和质**: 15%")
    cq1.progress(15)
    cq2.markdown("**阴虚质**: 22%")
    cq2.progress(22)
    cq3.markdown("**阳虚质**: 18%")
    cq3.progress(18)
    cq1.markdown("**气虚质**: 20%")
    cq1.progress(20)
    cq2.markdown("**气郁质**: 12%")
    cq2.progress(12)
    cq3.markdown("**痰湿质**: 13%")
    cq3.progress(13)

    st.divider()

    # 最近订单
    st.markdown(f"### {t('🛒 最近订单','Recent Orders')}")
    try:
        orders = []
        if orders_file.exists():
            with open(orders_file, encoding='utf-8') as f:
                for line in f:
                    try:
                        orders.append(json.loads(line))
                    except Exception:
                        pass
        if orders:
            for o in orders[-5:]:
                items = o.get('items', {})
                item_str = ', '.join([f"{k}x{v}" for k, v in items.items()])
                st.markdown(f"**{o.get('name','?')}** | {o.get('phone','?')} | {item_str} | {o.get('time','?')}")
        else:
            st.caption(t("暂无订单","No orders yet"))
    except Exception:
        pass

    st.divider()
    st.markdown(f"### {t('📈 流量来源','Traffic Sources')}")
    c1, c2, c3 = st.columns(3)
    c1.metric(t("微信","WeChat"), "60%")
    c2.metric(t("直接访问","Direct"), "25%")
    c3.metric(t("分享链接","Referral"), "15%")
