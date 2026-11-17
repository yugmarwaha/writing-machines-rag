"""Build, save, load, and search the vector index.

The "index" is just a NumPy matrix: one row of numbers (an embedding) per
fragment. With ~160 fragments, comparing a question against every row takes
microseconds, so no vector database is needed.
"""

import json

import numpy as np
import ollama

from . import config

VECTORS_FILE = "vectors.npy"
META_FILE = "meta.json"


def embed(texts, prefix):
    """Turn texts into unit-length vectors with the Ollama embedding model."""
    response = ollama.embed(model=config.EMBED_MODEL, input=[prefix + t for t in texts])
    vectors = np.array(response["embeddings"], dtype=np.float32)
    # Scaling every vector to length 1 makes a dot product equal cosine similarity.
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


def build_index(records, index_dir=config.INDEX_DIR):
    """Embed every record's `text` and save the vectors next to their IDs."""
    vectors = embed([r["text"] for r in records], config.DOC_PREFIX)
    index_dir.mkdir(parents=True, exist_ok=True)
    np.save(index_dir / VECTORS_FILE, vectors)
    meta = {"embed_model": config.EMBED_MODEL, "ids": [r["id"] for r in records]}
    (index_dir / META_FILE).write_text(json.dumps(meta), encoding="utf-8")
    return vectors


def load_index(records, index_dir=config.INDEX_DIR):
    """Load saved vectors, refusing an index that no longer matches the data or model."""
    meta_path = index_dir / META_FILE
    if not meta_path.exists():
        raise SystemExit("No index found. Run: python -m rag build")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta["embed_model"] != config.EMBED_MODEL or meta["ids"] != [r["id"] for r in records]:
        raise SystemExit("Index is out of date (data or embedding model changed). Run: python -m rag build")
    return np.load(index_dir / VECTORS_FILE)


def search(question, records, vectors, k=config.TOP_K, entrant=None):
    """Return the k records most similar to the question, as (score, record) pairs.

    If `entrant` is given, only that contributor's fragments are ranked.
    """
    query = embed([question], config.QUERY_PREFIX)[0]
    scores = vectors @ query
    wanted = entrant.strip().lower() if entrant else None
    candidates = [i for i, r in enumerate(records) if not wanted or r["entrant"].lower() == wanted]
    if not candidates:
        raise SystemExit(f"No fragments found for contributor {entrant!r}.")
    best = sorted(candidates, key=lambda i: scores[i], reverse=True)[:k]
    return [(float(scores[i]), records[i]) for i in best]
