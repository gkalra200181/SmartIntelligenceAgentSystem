"""
followup_agent.py

Agent that generates a clear follow-up message based on:
- summary
- refined action items
- risks
- themes
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from src.agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a Follow-Up Communication Agent.

Write a clear, concise follow-up message after a meeting that includes:
- a brief recap of what was discussed,
- a bullet list of action items (owner, description, due date, priority),
- a short note on any risks or recurring themes.

Tone: professional, calm, and specific.

Return plain text (no JSON).
"""


class FollowupAgent(BaseAgent):
    """Creates a human-readable follow-up email/message."""

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        summary: str = context.get("summary", "")
        actions: List[Dict[str, Any]] = context.get("actions", [])
        risks: List[str] = context.get("global_risks", [])
        themes: List[str] = context.get("themes", [])

        payload = {
            "summary": summary,
            "actions": actions,
            "risks": risks,
            "themes": themes,
        }

        user_msg = (
            "Use the following structured information to write the follow-up.\n\n"
            f"{json.dumps(payload, indent=2)}"
        )

        text = self.llm.chat(SYSTEM_PROMPT, [{"role": "user", "content": user_msg}])
        context["followup_message"] = text
        return context
