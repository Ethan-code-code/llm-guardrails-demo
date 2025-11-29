# llm_client.py
import os
from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

_client = None


def get_client() -> OpenAI:
    """Return a singleton OpenAI client using the OPENAI_API_KEY env var."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable is not set."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def call_llm(prompt: str) -> str:
    """Call the chat model with a simple system+user message."""
    client = get_client()
    completion = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.4,
    )
    return completion.choices[0].message.content
