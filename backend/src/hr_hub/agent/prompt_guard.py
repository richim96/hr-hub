"""Prompt safety guard submodule."""

import os

from groq import AsyncGroq

from hr_hub.agent import LOGGER


async def is_prompt_safe(message: str) -> bool:
    """Classify a user message as safe or a prompt-injection attempt.

    Calls the Groq API with ``meta-llama/llama-prompt-guard-2-22m``.
    Failed requests will be marked UNSAFE as a precaution.

    Args:
        message (str): Raw user input to evaluate.

    Returns:
        bool: ``True`` if the message is classified BENIGN, ``False`` if
            INJECTION is detected.
    """
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY", ""))

    try:
        response = await client.chat.completions.create(
            model="meta-llama/llama-prompt-guard-2-22m",
            messages=[{"role": "user", "content": message}],
        )
        label: str = (response.choices[0].message.content or "").strip().upper()
        LOGGER.info(f"Prompt guard verdict: {label!r}")
        return label == "BENIGN"
    except Exception as exc:
        LOGGER.warning(f"Prompt guard API call failed: {exc} — defaulting to UNSAFE")
        return False
