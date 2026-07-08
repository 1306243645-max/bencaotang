"""共享 API 工具 — 统一处理 DeepSeek 返回的 ThinkingBlock。"""

from anthropic.types import TextBlock, ThinkingBlock


def extract_text(content: list) -> str:
    """从 Anthropic API 的 response.content 中提取纯文本。

    自动跳过 ThinkingBlock（思考块），只取 TextBlock 的内容。
    """
    parts = []
    for block in content:
        if isinstance(block, TextBlock):
            parts.append(block.text)
        elif isinstance(block, ThinkingBlock):
            # 思考块不返回给工具调用者
            continue
    return "\n".join(parts)
