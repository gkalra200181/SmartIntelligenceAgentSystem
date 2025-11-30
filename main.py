"""
main.py

Demo script to run the MeetingOrchestrator on multiple sample transcripts.
This showcases:
- multi-agent pipeline
- memory across meetings
- trend insights
- evaluation metrics per meeting
"""

from __future__ import annotations
import os
from typing import List, Dict, Any

from src.orchestrator import MeetingOrchestrator


def load_transcript(path: str) -> str:
    """Load a transcript from the data folder."""
    if not os.path.exists(path):
        return f"[Transcript file not found: {path}]"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    # List of (file_path, metadata) pairs for multiple meetings
    meetings: List[Dict[str, Any]] = [
        {
            "path": os.path.join("data", "sample_transcript.txt"),
            "metadata": {
                "meeting_id": "meeting-001",
                "title": "Q4 Onboarding Release Planning",
                "participants": ["PM", "Engineer", "Designer", "QA Lead", "Support Lead"],
                "type": "Planning",
            },
        },
        {
            "path": os.path.join("data", "sample_transcript_2.txt"),
            "metadata": {
                "meeting_id": "meeting-002",
                "title": "Bug Triage & Incident Review",
                "participants": ["PM", "Engineer", "SRE", "Support Lead"],
                "type": "Bug Triage",
            },
        },
        {
            "path": os.path.join("data", "sample_transcript_3.txt"),
            "metadata": {
                "meeting_id": "meeting-003",
                "title": "Sprint Retrospective",
                "participants": ["PM", "Engineer", "Designer"],
                "type": "Retro",
            },
        },
    ]

    orchestrator = MeetingOrchestrator()

    last_context = None

    for idx, m in enumerate(meetings, start=1):
        print("\n" + "=" * 80)
        print(f"MEETING {idx}: {m['metadata']['title']}")
        print("=" * 80)

        transcript = load_transcript(m["path"])
        context = orchestrator.process_meeting(transcript, m["metadata"])
        last_context = context  # keep reference to the last run

        # Per-meeting outputs
        print("\n--- SUMMARY ---")
        print(context.get("summary", ""))

        print("\n--- ACTION ITEMS ---")
        for a in context.get("actions", []):
            owner = a.get("owner", "UNASSIGNED")
            desc = a.get("description", "")
            due = a.get("due_date", "TBD")
            prio = a.get("priority", "Medium")
            print(f"- [{prio}] {owner}: {desc} (Due: {due})")

        print("\n--- FOLLOW-UP MESSAGE (MARKDOWN) ---")
        print(context.get("followup_message", ""))

        print("\n--- EVALUATION METRICS ---")
        print(context.get("evaluation", {}))

    # After all meetings, show trend insights from the final context
    if last_context:
        print("\n" + "=" * 80)
        print("CROSS-MEETING TREND INSIGHTS")
        print("=" * 80)

        print("\nRecurring blockers:", last_context.get("recurring_blockers", []))
        print("Overloaded people:", last_context.get("overloaded_people", []))
        print("Themes:", last_context.get("themes", []))

        print("\nTotal meetings stored in memory:",
              len(orchestrator.memory.get_all_meetings()))
        print("Total actions across all meetings:",
              orchestrator.memory.total_actions())


if __name__ == "__main__":
    main()
