"""Download the sentence embedding model snapshot at container startup."""

import os

import huggingface_hub
import tqdm


def main() -> None:
    """Download the configured embedding model into the Hugging Face cache."""

    repo_id = os.getenv(
        "EMBEDDING_MODEL_NAME",
        "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    )
    token = os.getenv("HF_TOKEN")
    snapshot_download = getattr(huggingface_hub, "snapshot_download")

    print(f"Downloading embedding model snapshot: {repo_id}")
    local_path = snapshot_download(
        repo_id=repo_id,
        token=token or None,
        allow_patterns=[
            "modules.json",
            "config_sentence_transformers.json",
            "sentence_bert_config.json",
            "config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "README.md",
            "model.safetensors",
            "pytorch_model.bin",
            "1_Pooling/config.json",
        ],
        tqdm_class=tqdm.tqdm,
    )
    print(f"Embedding model cached at: {local_path}")


if __name__ == "__main__":
    main()
