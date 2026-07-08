"""本草堂 CSS styles."""

CSS = """<style>
    /* ═══════════ 本草堂 · 简约专业医疗风 ═══════════ */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    * { font-family: 'Noto Sans SC', 'PingFang SC', sans-serif !important; }
    :root {
        --primary: #2B7A4B; --primary-light: #E8F5E9;
        --text: #2D3436; --text-light: #636E72; --bg: #FAFBFB;
        --card: #FFFFFF; --border: #E8ECF0; --accent: #00B894;
    }
    .stApp, .main { background: var(--bg) !important; }
    section[data-testid="stSidebar"] {
        background: #FFFFFF !important; border-right: 1px solid var(--border) !important;
    }
    section[data-testid="stSidebar"] h2 { font-weight: 700 !important; color: var(--primary) !important; font-size: 1.4rem !important; }
    .nav-btn {
        display: inline-block; padding: 0.4rem 1rem; background: var(--card); color: var(--text) !important;
        font-weight: 500; text-align: center; cursor: pointer; transition: all 0.2s;
        text-decoration: none; font-size: 0.85rem; border: 1px solid var(--border); border-radius: 8px;
    }
    .nav-btn:hover { border-color: var(--primary); color: var(--primary) !important; }
    .nav-btn.active { background: var(--primary); color: white !important; border-color: var(--primary); }
    .service-card { background: var(--card); border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04); height: 100%; border: 1px solid var(--border); transition: all 0.2s; }
    .service-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); border-color: var(--primary-light); }
    .stButton button { border-radius: 8px !important; font-weight: 500 !important; background: var(--primary) !important; color: white !important; border: none !important; }
    .stButton button:hover { background: #236A3D !important; }
    hr { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }
    .stChatMessage { border-radius: 12px !important; border: 1px solid var(--border) !important; }
    .stMetric { background: var(--card) !important; border-radius: 8px !important; border: 1px solid var(--border) !important; }
    .stTabs [data-baseweb="tab-list"] { border-bottom: 2px solid var(--border) !important; }
    .stTabs [aria-selected="true"] { color: var(--primary) !important; border-bottom: 2px solid var(--primary) !important; }
</style>"""


def inject_css():
    """Inject the shared CSS into the Streamlit app."""
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)
