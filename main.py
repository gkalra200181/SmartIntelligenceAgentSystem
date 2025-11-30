"""
main.py

Demo script to run the MeetingOrchestrator on multiple sample transcripts.

- Reuses a single orchestrator so memory builds up across meetings.
- Prints summary, follow-up message, and evaluation metrics per meeting.
"""

from __future__ import annotations
import os
from typing import List

from src.orchestrator import MeetingOrchestrator


def load_transcript(path: str) -> str:
    """Load a transcript file, or return a fallback string if missing."""
    if not os.path.exists(path):
        return "This is a placeholder meeting transcript with minimal content."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main() -> None:
    # List of transcript files to process.
    # You can add/remove files here.
    transcript_files: List[str] = [
        os.path.join("data", "sample_transcript.txt"),       # your original
        os.path.join("data", "sample_transcript_1.txt"),     # add your own
        os.path.join("data", "sample_transcript_2.txt"),     # add your own
    ]

    orchestrator = MeetingOrchestrator()

    for idx, path in enumerate(transcript_files, start=1):
        print("\n" + "=" * 80)
        print(f"MEETING {idx}: {os.path.basename(path)}")
        print("=" * 80)

        transcript = load_transcript(path)
        metadata = {
            "meeting_id": f"meeting-{idx}",
            "source_file": path,
        }

        result = orchestrator.process_meeting(transcript, metadata)

        print("\n--- SUMMARY ---")
        print(result.get("summary", ""))

        print("\n--- FOLLOW-UP MESSAGE ---")
        print(result.get("followup_message", ""))

        print("\n--- EVALUATION METRICS ---")
        print(result.get("evaluation", {}))

        # Optionally show trend insights once multiple meetings have run
        if idx > 1:
            print("\n--- TREND INSIGHTS (AFTER THIS MEETING) ---")
            print("Recurring blockers:", result.get("recurring_blockers", []))
            print("Overloaded people:", result.get("overloaded_people", []))
            print("Themes:", result.get("themes", []))


if __name__ == "__main__":
    main()
