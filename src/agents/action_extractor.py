"""
action_extractor.py

Agent that extracts action items from a transcript + summary.
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from src.agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are an Action Item Extraction Agent.

From a meeting summary + transcript, extract a JSON list of action items.
Each action item MUST be an object with:
- "description": string
- "owner": string (person or role; use "UNASSIGNED" if unknown)
- "due_date": string (e.g. "next meeting", "TBD", or a relative date)
- "priority": string in ["High", "Medium", "Low"]

Return ONLY a JSON list. No surrounding text, no backticks.
"""


class ActionItemExtractorAgent(BaseAgent):
    """Extracts structured action items from a meeting."""

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        transcript: str = context["transcript"]
        summary: str = context.get("summary", "")

        user_msg = (
            "Extract clear action items from this meeting.\n\n"
            f"SUMMARY:\n{summary}\n\nTRANSCRIPT:\n{transcript}"
        )

        raw = self.llm.chat(SYSTEM_PROMPT, [{"role": "user", "content": user_msg}])
        context["actions_raw"] = raw

        actions: List[Dict[str, Any]] = []
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                actions = data
        except Exception:
            actions = []

        context["actions"] = actions
        return context
