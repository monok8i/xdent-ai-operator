"""AI answer orchestration for transcript-backed responses."""

from __future__ import annotations

import json
import re
import unicodedata
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.infra.ai.client import AIClient
    from src.infra.db.models import TranscriptTheme, Transcript
    from src.infra.db.repository import TranscriptRepository
    from src.service.search import SearchService


class AnswerService:
    """Select a theme, retrieve transcripts, and ask the AI for the final answer."""

    _SEARCH_LIMIT = 10
    _SEARCH_MAX_DISTANCE = 0.4
    _TRANSCRIPTS_FOR_PROMPT = 5

    _THEME_SYSTEM_PROMPT = (
        "You select the single best transcript theme for a user prompt. "
        'Return only valid JSON with this shape: {"theme_id": <integer>}. '
        "Use exactly one of the provided theme ids."
    )

    _ANSWER_SYSTEM_PROMPT = (
        "You answer support questions using only the provided transcript excerpts. "
        "Answer in the same language as the user prompt. "
        "Return only the final answer text, in one short paragraph. "
        "Do not mention that you searched transcripts. "
        "Do not invent details that are not present in the excerpts. "
        "If the excerpts are insufficient, give the most cautious and general answer supported by them."
    )

    def __init__(
        self,
        *,
        ai_client: "AIClient",
        repository: "TranscriptRepository",
        search_service: "SearchService",
    ) -> None:
        self._ai_client = ai_client
        self._repository = repository
        self._search_service = search_service

    async def answer(self, prompt: str) -> str:
        """Return the final AI answer for a user prompt."""

        themes = await self._repository.get_themes()
        theme = await self._select_theme(prompt, themes)

        hits = await self._search_service.search(
            theme_id=theme.id,
            prompt=prompt,
            limit=self._SEARCH_LIMIT,
            max_distance=self._SEARCH_MAX_DISTANCE,
        )

        excerpts = self._build_transcript_excerpts(hits)
        user_prompt = self._build_answer_prompt(
            prompt=prompt, theme=theme, excerpts=excerpts
        )

        return await self._ai_client.complete(
            system_prompt=self._ANSWER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

    async def _select_theme(
        self,
        prompt: str,
        themes: list[TranscriptTheme],
    ) -> TranscriptTheme:
        if not themes:
            raise RuntimeError("No transcript themes are available")

        themes_payload = "\n".join(f"{theme.id}: {theme.name}" for theme in themes)
        selection_prompt = (
            f"User prompt:\n{prompt}\n\n"
            f"Available themes:\n{themes_payload}\n\n"
            "Return only the JSON object with the best theme_id."
        )

        raw_response = await self._ai_client.complete(
            system_prompt=self._THEME_SYSTEM_PROMPT,
            user_prompt=selection_prompt,
            max_tokens=32,
            temperature=0.0,
        )

        theme_id = self._parse_theme_id(raw_response)
        if theme_id is not None:
            for theme in themes:
                if theme.id == theme_id:
                    return theme

        return self._fallback_theme(prompt, themes)

    def _fallback_theme(
        self,
        prompt: str,
        themes: list[TranscriptTheme],
    ) -> TranscriptTheme:
        prompt_tokens = self._tokenize(prompt)
        best_theme = themes[0]
        best_score = -1

        for theme in themes:
            score = len(prompt_tokens & self._tokenize(theme.name))
            if score > best_score:
                best_score = score
                best_theme = theme

        return best_theme

    @staticmethod
    def _parse_theme_id(raw_response: str) -> int | None:
        try:
            payload = json.loads(raw_response)
        except json.JSONDecodeError:
            match = re.search(r"\btheme_id\b\s*[:=]\s*(\d+)", raw_response)
            if match is None:
                return None

            return int(match.group(1))

        if isinstance(payload, dict):
            value = payload.get("theme_id")  # type: ignore

            if isinstance(value, int):
                return value

            if isinstance(value, str) and value.isdigit():
                return int(value)

        return None

    @classmethod
    def _tokenize(cls, text: str) -> set[str]:
        normalized = unicodedata.normalize("NFKD", text).casefold()
        stripped = "".join(
            character
            for character in normalized
            if not unicodedata.combining(character)
        )
        return set(re.findall(r"[a-z0-9]+", stripped))

    def _build_transcript_excerpts(
        self,
        hits: list[tuple[Transcript, float]],
    ) -> str:
        if not hits:
            return "No transcript excerpts were found for the selected theme."

        excerpts: list[str] = []
        for index, (transcript, distance) in enumerate(
            hits[: self._TRANSCRIPTS_FOR_PROMPT],
            start=1,
        ):
            clear_transcript = getattr(transcript, "clear_transcript", "")
            excerpts.append(
                f"{index}. distance={distance:.4f}\n{clear_transcript.strip()}"
            )

        return "\n\n".join(excerpts)

    def _build_answer_prompt(
        self, *, prompt: str, theme: TranscriptTheme, excerpts: str
    ) -> str:
        return (
            f"Selected theme: {theme.id} - {theme.name}\n\n"
            f"User prompt:\n{prompt}\n\n"
            f"Transcript excerpts:\n{excerpts}\n\n"
            "Write one short paragraph with the most accurate answer possible. "
            "Use only facts supported by the excerpts."
        )
