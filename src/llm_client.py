"""
llm_client.py

Abstraction layer for calling an LLM (e.g., Gemini).
Right now this has a mock implementation so the rest of
the system is testable without keys.

To integrate Gemini:
- Replace the mock `chat` method with real API calls.
"""

from typing import List, Dict


class LLMClient:
    """Simple wrapper around an LLM chat API."""

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.model_name = model_name

    def chat(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Combines a system prompt with a list of messages and
        returns the model's text response.

        Parameters
        ----------
        system_prompt : str
            Instructions describing the agent's role / behavior.
        messages : List[Dict[str, str]]
            Conversation messages with "role" and "content" keys.

        Returns
        -------
        str
            Model response as plain text.
        """
        # TODO: replace with a real Gemini call, e.g.:
        # model = genai.GenerativeModel(self.model_name)
        # response = model.generate_content([system_prompt] + [m["content"] for m in messages])
        # return response.text

        # Mock behavior for local / offline wiring.
        last_user = messages[-1]["content"] if messages else ""
        return f"[MOCK {self.model_name} RESPONSE] " + last_user[:200]
