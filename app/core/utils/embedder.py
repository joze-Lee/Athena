# athena/app/core/utils/embedder.py

from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import json

CHUNKS_DIR = Path("data/chunks")
INDEX_DIR = Path("data/indexes")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

def load_chunks():
    chunks = []
    metadata = []

    for chunk_file in CHUNKS_DIR.glob("*.txt"):
        text = chunk_file.read_text(encoding="utf-8").strip()
        chunks.append(text)
        metadata.append({
            "chunk_file": str(chunk_file),
            "text": text
        })

    return chunks, metadata

def embed_chunks():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    chunks, metadata = load_chunks()
    embeddings = model.encode(chunks, show_progress_bar=True)
    np.save(INDEX_DIR / "chunk_vectors.npy", embeddings)

    with open(INDEX_DIR / "chunk_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"[INFO] Saved {len(embeddings)} embeddings to {INDEX_DIR}")
