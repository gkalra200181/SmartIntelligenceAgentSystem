"""
transcript_analyzer.py

Agent that takes a raw meeting transcript and produces:
- topics
- key decisions
- a concise summary
"""

from __future__ import annotations
import json
from typing import Dict, Any

from src.agents.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a Meeting Transcript Analyzer.

Given a raw meeting transcript, you MUST return a JSON object with:
- "topics": a short list of 3-7 key topics (strings)
- "decisions": a short list of important decisions (strings)
- "summary": a concise 3-5 sentence summary of the meeting.

Return ONLY valid JSON. Do not include backticks.
"""


class TranscriptAnalyzerAgent(BaseAgent):
    """Analyzes a transcript and extracts high-level structure."""

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        transcript: str = context["transcript"]

        user_msg = (
            "Analyze the following meeting transcript and respond ONLY with JSON.\n\n"
            f"TRANSCRIPT:\n{transcript}"
        )
        raw = self.llm.chat(SYSTEM_PROMPT, [{"role": "user", "content": user_msg}])
        context["transcript_analysis_raw"] = raw

        topics, decisions, summary = [], [], ""

        try:
            data = json.loads(raw)
            topics = data.get("topics", [])
            decisions = data.get("decisions", [])
            summary = data.get("summary", "")
        except Exception:
            # Fallback if JSON parsing fails
            summary = "Automatic summary unavailable (JSON parse error)."

        context["topics"] = topics
        context["decisions"] = decisions
        context["summary"] = summary
        return context
