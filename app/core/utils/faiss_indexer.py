# athena/app/core/utils/faiss_indexer.py
import faiss
import numpy as np
from pathlib import Path
import json

INDEX_DIR = Path("data/indexes")

def build_faiss_index():
    vectors = np.load(INDEX_DIR / "chunk_vectors.npy")
    dim = vectors.shape[1]

    index = faiss.IndexFlatIP(dim)          # change based on output
    # before adding vectors to FAISS
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    index.add(vectors)                       # add all vectors

    faiss.write_index(index, str(INDEX_DIR / "faiss_index.bin"))
    print(f"[INFO] FAISS index built with {index.ntotal} vectors")

def load_index():
    return faiss.read_index(str(INDEX_DIR / "faiss_index.bin"))

def load_metadata():
    with open(INDEX_DIR / "chunk_metadata.json") as f:
        return json.load(f)

def search(query_embedding, top_k=5):
    index = load_index()
    metadata = load_metadata()
    D, I = index.search(query_embedding, top_k)   # distances, indices
    results = [metadata[i] for i in I[0]]
    return results, D[0]
