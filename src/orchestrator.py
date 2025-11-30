"""
orchestrator.py

Coordinates the multi-agent system:
- transcript analysis
- action extraction
- quality loop
- trend analysis using memory
- follow-up generation
- simple evaluation metrics (observability)
"""

from __future__ import annotations
from typing import Dict, Any, List
import logging
import time

from src.llm_client import LLMClient
from src.memory_store import InMemoryMeetingStore
from src.agents.transcript_analyzer import TranscriptAnalyzerAgent
from src.agents.action_extractor import ActionItemExtractorAgent
from src.agents.priority_risk_agent import PriorityRiskAgent
from src.agents.trend_agent import TrendAgent
from src.agents.followup_agent import FollowupAgent


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
)


class MeetingOrchestrator:
    """
    Central coordinator (sequential + loop agent behavior).

    This class represents the "multi-agent system" from the perspective
    of the competition rubric.
    """

    def __init__(self) -> None:
        self.llm = LLMClient()
        self.memory = InMemoryMeetingStore()

        # Sub-agents
        self.transcript_agent = TranscriptAnalyzerAgent(self.llm, "transcript_analyzer")
        self.action_agent = ActionItemExtractorAgent(self.llm, "action_extractor")
        self.priority_agent = PriorityRiskAgent(self.llm, "priority_risk")
        self.trend_agent = TrendAgent(self.llm, "trend_insights", self.memory)
        self.followup_agent = FollowupAgent(self.llm, "followup")

    def process_meeting(self, transcript: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the full agent pipeline for a single meeting.
        Returns the final context with all outputs.
        """

        start_time = time.time()
        context: Dict[str, Any] = {
            "transcript": transcript,
            "metadata": metadata,
        }

        logging.info("Starting transcript analysis...")
        context = self.transcript_agent.run(context)

        logging.info("Extracting action items...")
        context = self.action_agent.run(context)

        # Loop: refine until quality_score >= threshold or max passes reached.
        max_passes = 2
        desired_quality = 85
        for i in range(max_passes):
            logging.info("Priority & risk refinement pass %s...", i + 1)
            context = self.priority_agent.run(context)
            score = context.get("quality_score", 0)
            logging.info("Quality score after pass %s: %s", i + 1, score)
            if score >= desired_quality:
                break

        logging.info("Computing trend insights across meetings...")
        context = self.trend_agent.run(context)

        logging.info("Generating follow-up message...")
        context = self.followup_agent.run(context)

        # Persist current meeting into memory
        self.memory.add_meeting(
            summary=context.get("summary", ""),
            actions=context.get("actions", []),
            metadata=metadata,
        )

        # Simple evaluation / observability metrics
        context["evaluation"] = self._evaluate_meeting(context)
        context["processing_time_sec"] = round(time.time() - start_time, 3)

        logging.info("Meeting processing completed in %ss", context["processing_time_sec"])
        return context

    @staticmethod
    def _evaluate_meeting(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Very simple, transparent evaluation of action quality:
        - how many actions
        - how many with owners
        - how many with high priority
        """

        actions: List[Dict[str, Any]] = context.get("actions", [])
        total = len(actions)
        with_owner = sum(1 for a in actions if a.get("owner") and a["owner"] != "UNASSIGNED")
        high_priority = sum(1 for a in actions if a.get("priority") == "High")

        return {
            "total_actions": total,
            "actions_with_owner": with_owner,
            "actions_with_owner_pct": round((with_owner / total) * 100, 1) if total else 0.0,
            "high_priority_actions": high_priority,
        }
