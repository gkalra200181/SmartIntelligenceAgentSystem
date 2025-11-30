"""
main.py

Simple CLI-style demo script to run the orchestrator on a sample transcript.
"""

from __future__ import annotations
import os

from src.orchestrator import MeetingOrchestrator


def load_sample_transcript() -> str:
    """Load the sample transcript from the data folder."""
    path = os.path.join("data", "sample_transcript.txt")
    if not os.path.exists(path):
        return "This is a placeholder transcript. Two people discuss priorities and assign tasks."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    transcript = load_sample_transcript()
    metadata = {
        "meeting_id": "sample-meeting-001",
        "participants": ["PM", "Designer", "Engineer"],
        "type": "Sprint Planning",
    }

    orchestrator = MeetingOrchestrator()
    result = orchestrator.process_meeting(transcript, metadata)

    print("\n=== SUMMARY ===")
    print(result.get("summary", ""))

    print("\n=== FOLLOW-UP MESSAGE ===")
    print(result.get("followup_message", ""))

    print("\n=== EVALUATION METRICS ===")
    print(result.get("evaluation", {}))


if __name__ == "__main__":
    main()
