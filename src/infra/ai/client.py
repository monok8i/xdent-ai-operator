"""OpenAI-compatible chat client used for theme selection and answer generation."""

from __future__ import annotations

import asyncio
import json
import urllib.error
import urllib.request
from typing import Sequence


class AIClient:
    """Minimal async client for OpenAI-compatible chat completions."""

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str,
        model: str,
        timeout_seconds: int,
        default_temperature: float,
        default_max_tokens: int,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout_seconds = timeout_seconds
        self._default_temperature = default_temperature
        self._default_max_tokens = default_max_tokens

    async def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """Return a single chat completion message."""

        payload: dict[str, object] = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self._default_temperature
            if temperature is None
            else temperature,
            "max_tokens": self._default_max_tokens
            if max_tokens is None
            else max_tokens,
        }

        response = await asyncio.to_thread(self._post_json, payload)
        try:
            return str(response["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError("Unexpected AI response format") from error

    async def close(self) -> None:
        """Provided for interface symmetry with other app clients."""

        return None

    def _post_json(self, payload: dict[str, object]) -> dict[str, object]:
        if not self._api_key:
            raise RuntimeError("AI_API_KEY is not configured")

        request = urllib.request.Request(
            url=f"{self._base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        try:
            with urllib.request.urlopen(
                request, timeout=self._timeout_seconds
            ) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"AI request failed with HTTP {error.code}: {detail}"
            ) from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"AI request failed: {error.reason}") from error
