"""BaseAgent — 封装 Anthropic SDK，支持原生 Tool Use。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import anthropic
from anthropic.types import TextBlock, ThinkingBlock, ToolUseBlock

from config.settings import settings
from config.api_utils import extract_text as _extract_text


# ── Tool 定义 ──────────────────────────────────────────────

@dataclass
class Tool:
    """Agent 可调用的工具。"""
    name: str
    description: str
    input_schema: dict
    handler: Callable[..., str]


def make_tool_param(tool: Tool) -> dict:
    """将 Tool 转为 Anthropic API 要求的 tool 参数格式。"""
    return {
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.input_schema,
    }


# ── Response ───────────────────────────────────────────────

@dataclass
class AgentResponse:
    """Agent 调用的返回结构。"""
    content: str
    thinking: str = ""
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    tool_calls: list[dict] = field(default_factory=list)
    raw: Any = None


# ── BaseAgent ──────────────────────────────────────────────

class BaseAgent:
    """基于 Claude API 的 Agent 基类，支持 Tool Use。

    使用方式:
        agent = BaseAgent(system="你是一个有用的助手")
        agent.add_tool(search_tool)
        response = agent.chat("搜索最新消息")
    """

    def __init__(
        self,
        system: str = "You are a helpful AI assistant.",
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        max_tool_rounds: int = 8,
    ):
        self.system = system
        self.model = model or settings.ANTHROPIC_DEFAULT_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_tool_rounds = max_tool_rounds
        self._tools: dict[str, Tool] = {}

        self.client = anthropic.Anthropic(
            api_key=settings.ANTHROPIC_AUTH_TOKEN,
            base_url=settings.ANTHROPIC_BASE_URL,
        )

    # ── Tool 管理 ────────────────────────────────────────

    def add_tool(self, tool: Tool) -> None:
        """注册一个工具。"""
        self._tools[tool.name] = tool

    def remove_tool(self, name: str) -> None:
        """移除一个工具。"""
        self._tools.pop(name, None)

    @property
    def tool_params(self) -> list[dict]:
        """转为 API 格式的 tools 参数。"""
        return [make_tool_param(t) for t in self._tools.values()]

    # ── 核心调用 ────────────────────────────────────────

    @staticmethod
    def _extract_content(content: list) -> tuple[str, str, list[dict]]:
        """从 response.content 中提取文本/思考/工具调用。"""
        text_parts = []
        thinking_parts = []
        tool_calls = []
        for block in content:
            try:
                if isinstance(block, TextBlock):
                    text_parts.append(block.text)
                elif isinstance(block, ThinkingBlock):
                    thinking_parts.append(getattr(block, 'thinking', str(block)))
                elif isinstance(block, ToolUseBlock):
                    tool_calls.append({
                        "id": block.id,
                        "name": block.name,
                        "input": block.input if isinstance(block.input, dict) else {},
                    })
                elif hasattr(block, 'text'):
                    text_parts.append(block.text)
            except Exception:
                text_parts.append(str(block))
        return "\n".join(text_parts), "\n".join(thinking_parts), tool_calls

    def _execute_tools(self, tool_calls: list[dict]) -> list[dict]:
        """执行工具调用，返回 tool_result 字典列表。"""
        results = []
        for tc in tool_calls:
            tool = self._tools.get(tc["name"])
            if tool:
                try:
                    output = tool.handler(**tc["input"])
                except (TypeError, Exception) as e:
                    try:
                        output = tool.handler()
                    except Exception:
                        output = f"工具执行错误: {e}"
            else:
                output = f"未知工具: {tc['name']}"
            results.append({
                "type": "tool_result",
                "tool_use_id": tc["id"],
                "content": output,
            })
        return results

    def chat(
        self, message: str, history: list[dict] | None = None
    ) -> AgentResponse:
        """发送消息，自动处理 Tool Use 循环。"""
        messages: list[dict] = (history or []) + [{"role": "user", "content": message}]

        all_tool_calls: list[dict] = []
        final_text = ""
        thinking = ""
        response = None

        for _ in range(max(1, self.max_tool_rounds)):
            kwargs: dict = dict(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system,
                messages=messages,
            )
            if self._tools:
                kwargs["tools"] = self.tool_params

            response = self.client.messages.create(**kwargs)

            text, thinking, tool_calls = self._extract_content(response.content)
            all_tool_calls.extend(tool_calls)

            if tool_calls:

                # 把 assistant 的 tool_use 响应序列化为 dict 后加入对话
                serialized_content = []
                for block in response.content:
                    try:
                        if hasattr(block, 'model_dump'):
                            serialized_content.append(block.model_dump())
                        elif isinstance(block, dict):
                            serialized_content.append(block)
                        else:
                            serialized_content.append({"type": "text", "text": str(block)})
                    except Exception:
                        serialized_content.append({"type": "text", "text": str(block)})

                messages.append({
                    "role": "assistant",
                    "content": serialized_content,
                })
                # 执行工具，把结果加入对话
                tool_results = self._execute_tools(tool_calls)
                messages.append({
                    "role": "user",
                    "content": tool_results,
                })
            else:
                final_text = text
                break

        return AgentResponse(
            content=final_text or "(达到最大工具调用轮次，流程终止)",
            thinking=thinking,
            model=response.model,
            usage={
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
            },
            tool_calls=all_tool_calls,
            raw=response,
        )

    def stream(self, message: str):
        """流式发送消息（不含工具调用）。"""
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=self.system,
            messages=[{"role": "user", "content": message}],
        ) as stream:
            for text in stream.text_stream:
                yield text
