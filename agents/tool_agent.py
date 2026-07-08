"""ToolUseAgent — 预装搜索、文件、翻译、邮件发送的即用型智能体。"""

from agents.base import BaseAgent, Tool
from tools import web_search, read_file, write_file, translate, send_email


# ── 预定义工具 ────────────────────────────────────────────

SEARCH_TOOL = Tool(
    name="web_search",
    description="搜索互联网获取最新信息。适合查找公司、产品、新闻、市场信息。",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索关键词，英文关键词结果更准确",
            },
            "max_results": {
                "type": "integer",
                "description": "返回结果数量（默认5，最多10）",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    handler=web_search,
)

READ_TOOL = Tool(
    name="read_file",
    description="读取本地文件内容。",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
        },
        "required": ["path"],
    },
    handler=lambda path: read_file(path),
)

WRITE_TOOL = Tool(
    name="write_file",
    description="将内容写入本地文件。",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "文件路径"},
            "content": {"type": "string", "description": "要写入的内容"},
        },
        "required": ["path", "content"],
    },
    handler=lambda path, content: write_file(path, content) or "写入成功",
)

TRANSLATE_TOOL = Tool(
    name="translate",
    description="将文本翻译为目标语言。中英双向或其他语种均可。",
    input_schema={
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "要翻译的文本"},
            "target_lang": {
                "type": "string",
                "description": "目标语言: 'English' 'Chinese' 'Japanese' 'French' 等",
                "default": "English",
            },
        },
        "required": ["text", "target_lang"],
    },
    handler=translate,
)

EMAIL_TOOL = Tool(
    name="send_email",
    description=(
        "发送邮件。需先在 .env 中配置 EMAIL_SENDER 和 EMAIL_PASSWORD。"
        "未配置时会返回提示信息而不是报错。"
    ),
    input_schema={
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "收件人邮箱，多个用逗号分隔"},
            "subject": {"type": "string", "description": "邮件主题"},
            "body": {"type": "string", "description": "邮件正文"},
            "cc": {"type": "string", "description": "抄送（可选）", "default": ""},
            "html": {
                "type": "boolean",
                "description": "是否 HTML 格式（默认 false = 纯文本）",
                "default": False,
            },
        },
        "required": ["to", "subject", "body"],
    },
    handler=send_email,
)


def create_tool_agent(
    system: str | None = None,
    include_email: bool = True,
    **kwargs,
) -> BaseAgent:
    """创建预装全工具链的 Agent。

    Args:
        system: 自定义系统提示词
        include_email: 是否注册邮件发送工具
        **kwargs: 传给 BaseAgent 的其他参数

    Returns:
        已注册工具链的 BaseAgent 实例
    """
    default_system = (
        "你是一个高效的 AI 助手，具备以下能力:\n"
        "- web_search: 搜索互联网获取最新信息\n"
        "- read_file / write_file: 读写本地文件\n"
        "- translate: 翻译文本（中英双向及各语种）\n"
        "- send_email: 发送邮件\n\n"
        "使用规则:\n"
        "1. 需要最新信息时搜索，搜不到就用知识回答\n"
        "2. 涉及翻译任务时使用 translate 工具\n"
        "3. 发邮件前先确认内容，发送后报告结果\n"
        "4. 重要结果用 write_file 保存\n"
        "5. 用中文回复，除非用户要求其他语言"
    )

    agent = BaseAgent(
        system=system or default_system,
        max_tokens=8192,
        max_tool_rounds=10,
        **kwargs,
    )
    agent.add_tool(SEARCH_TOOL)
    agent.add_tool(READ_TOOL)
    agent.add_tool(WRITE_TOOL)
    agent.add_tool(TRANSLATE_TOOL)
    if include_email:
        agent.add_tool(EMAIL_TOOL)
    return agent
