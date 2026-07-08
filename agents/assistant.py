"""AssistantAgent — 通用助手智能体，带对话记忆。"""

from agents.base import BaseAgent, AgentResponse


class AssistantAgent(BaseAgent):
    """带对话历史的通用助手。

    使用方式:
        assistant = AssistantAgent(name="小焊", role="焊接机器人出口业务助手")
        response = assistant.chat("帮我写一封澳洲客户的英文邮件")
    """

    def __init__(self, name: str = "Assistant", role: str = "通用AI助手", **kwargs):
        system_prompt = (
            f"你是 {name}，一个专业的{role}。\n"
            "请始终保持专业、准确、有帮助。使用简洁清晰的表达。"
        )
        super().__init__(system=system_prompt, **kwargs)
        self.name = name
        self.role = role
        self.history: list[dict] = []

    def chat(self, message: str) -> AgentResponse:
        """发送消息（自动维护对话历史）。"""
        response = super().chat(message, history=self.history)
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": response.content})
        return response

    def clear_history(self):
        """清空对话历史。"""
        self.history = []
