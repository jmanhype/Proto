"""OpenAI ChatGPT integration for conversational AI."""

from typing import List, Dict, Any
from openai import OpenAI


class ChatGPT:
    """
    ChatGPT wrapper for conversational interactions.

    This class manages dialogue history and handles streaming/non-streaming
    responses from OpenAI's GPT-3.5-turbo model.

    Attributes:
        client (OpenAI): OpenAI API client instance
        dialogue_history (List[Dict[str, str]]): Conversation history with roles and content
        valid_stream (bool): Whether to use streaming responses
    """

    def __init__(self, valid_stream: bool) -> None:
        """
        Initialize the ChatGPT client.

        Args:
            valid_stream: If True, responses will be streamed; otherwise, complete responses
        """
        self.client = OpenAI()
        self.dialogue_history: List[Dict[str, str]] = []
        self.valid_stream = valid_stream

    def get(self, user_utterance: str) -> Any:
        """
        Send a user message and get a response from ChatGPT.

        Args:
            user_utterance: The user's text input

        Returns:
            OpenAI completion object (streaming or non-streaming depending on configuration)
        """
        self.dialogue_history.append({"role": "user", "content": user_utterance})
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.dialogue_history,
            stream=self.valid_stream
        )
        return completion

    def set_agent_utterance(self, agent_utterance: str) -> None:
        """
        Manually add an assistant response to the dialogue history.

        Args:
            agent_utterance: The assistant's response text
        """
        self.dialogue_history.append({"role": "assistant", "content": agent_utterance})