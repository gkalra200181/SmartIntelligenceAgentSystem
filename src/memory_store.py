"""
memory_store.py

Very simple in-memory "long-term" store for meetings.
In a real deployment this could be a database or vector store.
"""

from __future__ import annotations
from collections import defaultdict
from typing import List, Dict, Any


class InMemoryMeetingStore:
    """
    Stores meetings and provides simple analytics across them.
    """

    def __init__(self) -> None:
        # Each meeting is a dict with keys: summary, actions, metadata.
        self.meetings: List[Dict[str, Any]] = []

    def add_meeting(
        self,
        summary: str,
        actions: List[Dict[str, Any]],
        metadata: Dict[str, Any],
    ) -> None:
        """Append a completed meeting record to memory."""
        self.meetings.append(
            {
                "summary": summary,
                "actions": actions,
                "metadata": metadata,
            }
        )

    def get_all_meetings(self) -> List[Dict[str, Any]]:
        """Return all stored meetings."""
        return list(self.meetings)

    def compute_owner_stats(self) -> Dict[str, int]:
        """
        Compute how many actions have been assigned to each owner
        across all meetings.
        """
        counts: Dict[str, int] = defaultdict(int)
        for meeting in self.meetings:
            for action in meeting.get("actions", []):
                owner = action.get("owner") or "UNASSIGNED"
                counts[owner] += 1
        return dict(counts)

    def total_actions(self) -> int:
        """Total number of actions across all meetings."""
        return sum(len(m.get("actions", [])) for m in self.meetings)
