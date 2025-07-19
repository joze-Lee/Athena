# core/utils/reranker.py

from sentence_transformers import CrossEncoder

# Load once globally
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank_chunks(query: str, chunks: list[str], top_k=5):
    # Create query-chunk pairs
    # pairs = [(query, chunk) for chunk in chunks]
    pairs = [(query, chunk["text"]) for chunk in chunks]

    # Get relevance scores
    scores = reranker.predict(pairs)
    # Attach scores to each chunk
    for i, score in enumerate(scores):
        chunks[i]["score"] = float(score)

    # Sort chunks by score
    # sorted_chunks = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)
    sorted_chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)
    
    return sorted_chunks[:top_k]
