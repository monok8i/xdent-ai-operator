"""Shared sentence embedding client used by the application."""

import asyncio
from typing import Sequence

from sentence_transformers import SentenceTransformer

from .exceptions import EmbeddingError


class SentenceTransformerEmbeddingClient:
    """Generate embeddings with a cached SentenceTransformer model.

    The model is loaded once during FastAPI startup and reused across requests.
    Embedding generation is executed in a worker thread so the event loop stays
    responsive while the model performs CPU or GPU work.
    """

    def __init__(
        self,
        *,
        model_name: str,
        device: str | None = None,
        normalize_embeddings: bool = True,
        batch_size: int,
    ) -> None:
        """Load the embedding model and store generation settings.

        Args:
            model_name: Hugging Face model identifier.
            device: Optional device override such as ``cpu`` or ``cuda``.
            normalize_embeddings: Whether to return normalized vectors.
            batch_size: Batch size used by the encoder.

        Raises:
            EmbeddingError: If model loading fails.
        """

        self._model_name = model_name
        self._device = device
        self._normalize_embeddings = normalize_embeddings
        self._batch_size = batch_size

        try:
            if device is None:
                self._model = SentenceTransformer(model_name)
            else:
                self._model = SentenceTransformer(model_name, device=device)
        except Exception as e:  # pragma: no cover - startup failure path
            raise EmbeddingError(
                f"Failed to load embedding model '{model_name}': {e}"
            ) from e

    async def generate_embeddings(self, texts: Sequence[str]) -> list[list[float]]:
        """Return embeddings for the supplied texts in input order.

        Args:
            texts: Sequence of input strings to embed.

        Returns:
            Embedding vectors in the same order as ``texts``.

        Raises:
            EmbeddingError: If the model fails to encode the supplied texts.
        """

        if not texts:
            return []

        cleaned_texts = [text.replace("\n", " ").strip() for text in texts]

        try:
            embeddings = await asyncio.to_thread(
                self._model.encode,  # type: ignore
                cleaned_texts,
                batch_size=min(len(cleaned_texts), self._batch_size),
                convert_to_numpy=True,
                normalize_embeddings=self._normalize_embeddings,
                show_progress_bar=False,
            )
            return embeddings.tolist()

        except Exception as e:
            raise EmbeddingError(f"Sentence embedding generation error: {e}") from e
