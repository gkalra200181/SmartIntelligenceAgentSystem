"""
priority_risk_agent.py

Agent that validates and refines action items:
- checks clarity
- flags risks
- computes a quality score for loop-based refinement.
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from src.agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a Priority & Risk Evaluation Agent.

Given a list of action items, you will:
1. Ensure each action is specific and actionable.
2. Ensure each action has an owner and priority.
3. Identify any risks or ambiguities.

You MUST return a JSON object with:
- "actions": refined list of action items (same structure as input)
- "global_risks": list of strings describing major risks / concerns
- "quality_score": integer 0-100 indicating clarity & readiness.

Return ONLY JSON, no extra text, no backticks.
"""


class PriorityRiskAgent(BaseAgent):
    """Refines actions and computes a quality score used by the loop agent."""

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        actions: List[Dict[str, Any]] = context.get("actions", [])

        user_msg = (
            "Evaluate and refine the following action items.\n\n"
            f"ACTIONS:\n{json.dumps(actions, indent=2)}"
        )

        raw = self.llm.chat(SYSTEM_PROMPT, [{"role": "user", "content": user_msg}])
        context["actions_validated_raw"] = raw

        refined_actions: List[Dict[str, Any]] = actions
        global_risks: List[str] = []
        quality_score: int = 50

        try:
            data = json.loads(raw)
            refined_actions = data.get("actions", actions)
            global_risks = data.get("global_risks", [])
            quality_score = int(data.get("quality_score", 50))
        except Exception:
            pass

        context["actions"] = refined_actions
        context["global_risks"] = global_risks
        context["quality_score"] = quality_score
        return context
