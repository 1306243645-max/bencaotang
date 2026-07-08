"""翻译工具 — 基于现有 LLM API，支持中英双向及多语种。"""

import anthropic
from config.settings import settings
from config.api_utils import extract_text

_client = anthropic.Anthropic(
    api_key=settings.ANTHROPIC_AUTH_TOKEN,
    base_url=settings.ANTHROPIC_BASE_URL,
)
MODEL = settings.ANTHROPIC_DEFAULT_MODEL


def translate(text: str, target_lang: str = "English") -> str:
    """将文本翻译为目标语言。

    Args:
        text: 要翻译的文本
        target_lang: 目标语言，如 'English' 'Chinese' 'Japanese' 'French' 等

    Returns:
        翻译后的文本
    """
    if not text.strip():
        return "(空文本)"

    try:
        response = _client.messages.create(
            model=MODEL,
            max_tokens=min(len(text) * 3, 4096),
            temperature=0.1,
            system="You are a professional translator. Output only the translation, no explanations.",
            messages=[{
                "role": "user",
                "content": f"Translate to {target_lang}:\n\n{text}",
            }],
        )
        return extract_text(response.content).strip()
    except Exception as e:
        return f"[翻译失败: {e}]"
