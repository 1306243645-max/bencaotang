"""AI 员工基类 — 统一的员工接口"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable
import json

from agents.base import BaseAgent, Tool

ROOT = Path(__file__).parent.parent.parent
OUTPUT = ROOT / "output" / "employees"


@dataclass
class EmployeeConfig:
    """员工配置"""
    name: str                          # 中文名
    role: str                          # 职位
    emoji: str                         # 头像 emoji
    system_prompt: str                 # 系统提示词
    daily_tasks: list[str] = field(default_factory=list)  # 每日任务清单


class AIEmployee:
    """AI 员工基类。

    每个员工有：
    - 身份（名字、职位、性格）
    - 技能（知识库工具）
    - 每日任务清单
    - 工作日志
    """

    def __init__(self, config: EmployeeConfig, model: str = None, max_tokens: int = 4096):
        self.config = config
        self.agent = BaseAgent(
            system=config.system_prompt,
            model=model,
            max_tokens=max_tokens,
            max_tool_rounds=5,
        )
        self._tools: dict[str, Tool] = {}
        self.log: list[dict] = []

    # ── 工具管理 ──────────────────────────────────────────

    def add_tool(self, tool: Tool):
        self._tools[tool.name] = tool
        self.agent.add_tool(tool)

    # ── 核心工作方法 ──────────────────────────────────────

    def work(self, task: str, context: str = "") -> str:
        """分配任务给员工，返回工作结果"""
        prompt = f"【任务】{task}"
        if context:
            prompt += f"\n\n【背景信息】{context}"
        prompt += "\n\n请认真完成以上任务，输出结果。"

        response = self.agent.chat(prompt)
        result = response.content

        # 记录日志
        self.log.append({
            "time": datetime.now().isoformat(),
            "task": task,
            "result": result[:500],
            "tokens": response.usage,
        })
        return result

    # ── 每日例会 ──────────────────────────────────────────

    def morning_briefing(self) -> str:
        """早会：今天要做什么"""
        tasks_text = "\n".join(f"- {t}" for t in self.config.daily_tasks)
        return self.work(
            f"今天是{datetime.now().strftime('%Y年%m月%d日 %A')}。"
            f"请根据你的职责，列出今天的具体执行计划：\n{tasks_text}",
            context=f"你是{self.config.name}，{self.config.role}。"
        )

    def evening_report(self, work_done: str = "") -> str:
        """晚会：今天做了什么"""
        return self.work(
            f"今天的工作已完成。请写一份简短的工作日报（100字以内），"
            f"包含：完成事项、数据亮点、明天重点。\n\n今日完成：{work_done}"
        )

    # ── 日志保存 ──────────────────────────────────────────

    def save_log(self):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        log_file = OUTPUT / f"{self.config.name}_{datetime.now():%Y%m%d}.json"
        log_file.write_text(
            json.dumps({"employee": self.config.name, "role": self.config.role,
                        "date": datetime.now().isoformat(), "log": self.log},
                       ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return log_file

    def __repr__(self):
        return f"{self.config.emoji} {self.config.name} — {self.config.role}"
