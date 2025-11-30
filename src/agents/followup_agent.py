"""
followup_agent.py

Agent that generates a clear, formatted follow-up message based on:
- summary
- refined action items
- risks
- themes

The output is a GitHub/Kaggle-friendly Markdown email:
- Subject line
- Greeting
- Summary section
- Action items as a Markdown table
- Risks / Themes
- Closing
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from src.agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a Follow-Up Communication Agent.

Your job is to write a clear, professional follow-up email after a meeting,
using GitHub-flavored Markdown so it renders nicely in notebooks and README files.

Use this output structure:

1. A subject line starting with: "Subject: ..."
2. A greeting, e.g. "Hi Team,"
3. A short paragraph summarizing the meeting.
4. A section titled "Summary" (as a Markdown heading, e.g. "### Summary")
5. A section titled "Action Items" with a Markdown table:

   | Owner | Task Description | Due Date | Priority |
   |-------|------------------|----------|----------|
   | ...   | ...              | ...      | ...      |

6. A section titled "Risks & Themes" with bullet points. If there are none, say "No major risks identified."
7. A short closing paragraph and sign-off.

Rules:
- The tone should be concise, calm, and professional.
- Use Markdown headings (###) and bullet points where appropriate.
- Use the structured data provided (summary, actions, risks, themes).
- If actions list is empty, explicitly say there were no concrete action items, and optionally suggest next steps.
- Do NOT return JSON.
- Do NOT wrap the output in backticks or code fences.
"""


class FollowupAgent(BaseAgent):
    """Creates a human-readable, Markdown-formatted follow-up email."""

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
            "Use the following structured information to write the Markdown email.\n\n"
            f"{json.dumps(payload, indent=2)}"
        )

        text = self.llm.chat(SYSTEM_PROMPT, [{"role": "user", "content": user_msg}])
        context["followup_message"] = text
        return context
