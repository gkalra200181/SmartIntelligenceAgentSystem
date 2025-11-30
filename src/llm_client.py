"""
llm_client.py

Abstraction layer for calling Gemini (or other LLMs).

IMPORTANT:
- Do NOT put your API key in this file.
- Set GEMINI_API_KEY using an environment variable in Kaggle or your local machine.
- This file is safe to commit to GitHub.
"""

import os
from typing import List, Dict
import google.generativeai as genai


class LLMClient:
    """
    Simple wrapper around a Gemini model for multi-agent calls.
    """

    def __init__(self, model_name: str = "gemini-3-pro"):
        self.model_name = model_name

        # Configure Gemini with API key FROM ENVIRONMENT VARIABLE ONLY.
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set.\n"
                "Please set it in your Kaggle notebook before running:\n"
                "os.environ['GEMINI_API_KEY'] = 'your-key-here'"
            )

        genai.configure(api_key=api_key)

        # Create a model instance.
        self.model = genai.GenerativeModel(self.model_name)

    def chat(self, system_prompt: str, messages: List[Dict[str, str]]) -> str:
        """
        Combines a system prompt with chat messages and sends them to Gemini.

        Parameters
        ----------
        system_prompt : str
            High-level instruction (agent role).
        messages : List[Dict[str, str]]
            Conversation messages with fields:
            - role: "user" or "assistant"
            - content: text content

        Returns
        -------
        str
            Model-generated text response.
        """
        # Construct a full prompt where the system prompt comes first
        # and user content follows.
        full_prompt = system_prompt.strip() + "\n\n"

        for m in messages:
            role = m.get("role", "user").upper()
            content = m.get("content", "")
            full_prompt += f"{role}: {content}\n"

        # Send the composed prompt to Gemini
        response = self.model.generate_content(full_prompt)

        # Return plain text
        return response.text
