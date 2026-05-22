"""Environment settings for the sentence embedding client."""

from src.core.config.env import BaseEnvConfig


class Config(BaseEnvConfig):
    """Model and runtime settings for sentence embeddings.

    Attributes:
        EMBEDDING_MODEL_NAME: Hugging Face model identifier used for text embeddings.
        EMBEDDING_DEVICE: Optional device override for model execution.
        EMBEDDING_NORMALIZE: Whether to L2-normalize embeddings before returning them.
    """

    EMBEDDING_MODEL_NAME: str = (
        "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    EMBEDDING_DEVICE: str | None = None
    EMBEDDING_NORMALIZE: bool = True
    EMBEDDING_BATCH_SIZE: int = 100
