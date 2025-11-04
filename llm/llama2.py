"""Llama2 local model integration for conversational AI."""

from typing import Any, Union, Dict, Iterator
from llama_cpp import Llama


class Llama2:
    """
    Llama2 wrapper for local conversational AI.

    This class provides an interface to the Llama2 model via llama-cpp-python,
    supporting both streaming and non-streaming responses.

    Attributes:
        llama (Llama): Llama model instance
        valid_stream (bool): Whether to use streaming responses
    """

    def __init__(self, valid_stream: bool = True) -> None:
        """
        Initialize the Llama2 model.

        Args:
            valid_stream: If True, responses will be streamed; defaults to True

        Note:
            Model expects to be at 'llm/models/elyza-q8.gguf'
            Uses 50 GPU layers by default for acceleration
        """
        self.llama = Llama(model_path="llm/models/elyza-q8.gguf", n_gpu_layers=50)
        self.valid_stream = valid_stream

    def get(self, user_utterance: str) -> Union[Dict[str, Any], Iterator[Dict[str, Any]]]:
        """
        Send a user message and get a response from Llama2.

        Args:
            user_utterance: The user's text input

        Returns:
            Response from Llama2 (dict or iterator depending on stream setting)

        Note:
            Uses Japanese system prompt: "あなたはアシスタントです。" (You are an assistant.)
        """
        streamer = self.llama.create_chat_completion(
            [{"role": "user", "content": f"""[INST] <<SYS>>\nあなたはアシスタントです。\n<</SYS>>\n\n{user_utterance}[/INST]"""}],
            stream=self.valid_stream
        )
        return streamer

    def set_agent_utterance(self, agent_utterance: str) -> None:
        """
        Manually add an assistant response (currently not implemented for Llama2).

        Args:
            agent_utterance: The assistant's response text

        Note:
            This method is a placeholder for API compatibility with ChatGPT class
        """
        pass