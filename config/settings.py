"""配置加载模块 — 支持 .env 和 Streamlit Cloud secrets。"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env（本地开发）
load_dotenv(Path(__file__).parent.parent / ".env")


def _get_secret(key: str, default: str = "") -> str:
    """优先读 Streamlit Cloud secrets，fallback 到环境变量。"""
    try:
        import streamlit as st
        val = st.secrets.get(key, "")
        if val:
            return val
    except Exception:
        pass
    return os.getenv(key, default)


class Settings:
    """AI Agent 工作站全局配置。"""

    # Anthropic
    ANTHROPIC_AUTH_TOKEN: str = _get_secret("ANTHROPIC_AUTH_TOKEN", "")
    ANTHROPIC_BASE_URL: str = _get_secret("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    ANTHROPIC_DEFAULT_MODEL: str = _get_secret("ANTHROPIC_DEFAULT_MODEL", "claude-sonnet-4-6")

    # OpenAI（可选）
    OPENAI_API_KEY: str = _get_secret("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = _get_secret("OPENAI_BASE_URL", "https://api.openai.com/v1")

    @classmethod
    def info(cls) -> str:
        """打印当前配置概览（隐藏敏感信息）。"""
        return (
            f"Base URL: {cls.ANTHROPIC_BASE_URL}\n"
            f"Model:    {cls.ANTHROPIC_DEFAULT_MODEL}\n"
            f"Token:    {'***' + cls.ANTHROPIC_AUTH_TOKEN[-8:] if cls.ANTHROPIC_AUTH_TOKEN else 'NOT SET'}"
        )


settings = Settings()
