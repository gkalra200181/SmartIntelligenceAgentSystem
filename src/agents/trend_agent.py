"""
trend_agent.py

Agent that uses current meeting + historical memory to detect:
- recurring blockers
- overloaded owners
- long-running themes
"""

from __future__ import annotations
import json
from typing import Dict, Any

from src.agents.base_agent import BaseAgent
from src.memory_store import InMemoryMeetingStore


SYSTEM_PROMPT = """
You are a Trend Insight Agent.

You are given:
- A history of past meetings (summaries + actions + metadata).
- The current meeting summary and actions.

You MUST return a JSON object with:
- "recurring_blockers": list of strings
- "overloaded_people": list of strings (owners overloaded with too many actions)
- "themes": list of strings representing long-running patterns.

Focus on high-level patterns rather than repetition.
Return ONLY JSON, no extra text.
"""


class TrendAgent(BaseAgent):
    """Detects trends across meetings using memory."""

    def __init__(
        self,
        llm: InMemoryMeetingStore | Any,  # type: ignore
        name: str,
        memory_store: InMemoryMeetingStore,
    ) -> None:
        # type: ignore because llm type is actually LLMClient; kept flexible for ADK.
        super().__init__(llm, name)
        self.memory_store = memory_store

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        history = self.memory_store.get_all_meetings()
        owner_stats = self.memory_store.compute_owner_stats()

        user_msg = (
            "You are given a history of meetings and the current one.\n\n"
            f"HISTORY:\n{json.dumps(history, indent=2)}\n\n"
            f"OWNER_STATS:\n{json.dumps(owner_stats, indent=2)}\n\n"
            "CURRENT_MEETING:\n"
            f"{json.dumps({'summary': context.get('summary', ''), 'actions': context.get('actions', [])}, indent=2)}"
        )

        raw = self.llm.chat(SYSTEM_PROMPT, [{"role": "user", "content": user_msg}])
        context["trend_insights_raw"] = raw

        recurring_blockers = []
        overloaded_people = []
        themes = []

        try:
            data = json.loads(raw)
            recurring_blockers = data.get("recurring_blockers", [])
            overloaded_people = data.get("overloaded_people", [])
            themes = data.get("themes", [])
        except Exception:
            pass

        context["recurring_blockers"] = recurring_blockers
        context["overloaded_people"] = overloaded_people
        context["themes"] = themes
        return context
