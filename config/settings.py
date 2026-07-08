"""配置加载模块 — 从 .env 读取并验证 API 配置。"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载项目根目录的 .env
load_dotenv(Path(__file__).parent.parent / ".env")


class Settings:
    """AI Agent 工作站全局配置。"""

    # Anthropic
    ANTHROPIC_AUTH_TOKEN: str = os.getenv("ANTHROPIC_AUTH_TOKEN", "")
    ANTHROPIC_BASE_URL: str = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
    ANTHROPIC_DEFAULT_MODEL: str = os.getenv("ANTHROPIC_DEFAULT_MODEL", "claude-sonnet-4-6")

    # OpenAI（可选）
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    @classmethod
    def info(cls) -> str:
        """打印当前配置概览（隐藏敏感信息）。"""
        return (
            f"Base URL: {cls.ANTHROPIC_BASE_URL}\n"
            f"Model:    {cls.ANTHROPIC_DEFAULT_MODEL}\n"
            f"Token:    {'***' + cls.ANTHROPIC_AUTH_TOKEN[-8:] if cls.ANTHROPIC_AUTH_TOKEN else 'NOT SET'}"
        )


settings = Settings()
