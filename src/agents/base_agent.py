"""
base_agent.py

Shared abstract base class for all agents.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any

from src.llm_client import LLMClient


class BaseAgent(ABC):
    """
    Base class for all agents.

    Each agent receives and returns a shared `context` dict.
    The orchestrator coordinates agent execution.
    """

    def __init__(self, llm: LLMClient, name: str) -> None:
        self.llm = llm
        self.name = name

    @abstractmethod
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implement agent logic and return updated context."""
        raise NotImplementedError
