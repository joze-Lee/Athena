# athena/app/main.py

import os
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from core.utils.pdf_parser import process_pdf
from core.utils.embedder import embed_chunks
from core.utils.faiss_indexer import build_faiss_index, search
from core.utils.reranker import rerank_chunks  


PDF_DIR = Path("data/pdfs")
CHUNK_OUTPUT_DIR = Path("data/chunks")

def process_all_pdfs():
    for file in PDF_DIR.glob("*.pdf"):
        process_pdf(file, CHUNK_OUTPUT_DIR)

def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("\n💡 Ask me anything about the PDFs (type 'exit' to quit):")
    while True:
        query = input("\n🔎 Your question: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("👋 Exiting. Have a great day!")
            break

        # Encode query
        q_vec = model.encode([query])
        q_vec = q_vec / np.linalg.norm(q_vec, axis=1, keepdims=True)

        # Search FAISS
        results, scores = search(q_vec, top_k=10)

        # Attach similarity scores to chunks
        top_chunks = [{"text": r["text"], "score": s} for r, s in zip(results, scores)]

        # Rerank with cross-encoder or custom model
        reranked = rerank_chunks(query, top_chunks, top_k=5)  # ✅ Apply reranker


        print("\n📌 Top reranked chunks:")
        for item in reranked:
            print(f"- ({item['score']:.4f}) {item['text'][:120]}…")  # Truncated tex


if __name__ == "__main__":
    process_all_pdfs()
    embed_chunks()
    build_faiss_index()
    main()
