"""
transcript_analyzer.py

Agent that takes a raw meeting transcript and produces:
- topics
- key decisions
- a concise summary

If the model does not return valid JSON, we gracefully fall back:
- use the raw response as the summary
- leave topics/decisions empty
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

Rules:
- Return ONLY valid JSON. Do not include backticks.
- Do not wrap the JSON in any explanation.
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

        topics = []
        decisions = []
        summary = ""

        # Try strict JSON parsing first
        try:
            data = json.loads(raw)
            topics = data.get("topics", []) or []
            decisions = data.get("decisions", []) or []
            summary = data.get("summary", "") or ""
        except Exception:
            # If parsing fails, treat the entire raw response as a summary
            summary = raw.strip()

        # Final safety fallback
        if not summary:
            summary = "Summary unavailable. The model did not provide a usable response."

        context["topics"] = topics
        context["decisions"] = decisions
        context["summary"] = summary
        return context
