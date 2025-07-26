# athena/app/core/utils/embedder.py

from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
import shutil

CHUNKS_DIR = Path("data/chunks")
INDEX_DIR = Path("data/indexes")
FAISS_INDEX_DIR =  Path("data/indexes/faiss_index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

# def load_chunks():
#     chunks = []
#     metadata = []

#     for chunk_file in CHUNKS_DIR.glob("*.txt"):
#         text = chunk_file.read_text(encoding="utf-8").strip()
#         chunks.append(text)
#         metadata.append({
#             "chunk_file": str(chunk_file),
#             "text": text
#         })

#     return chunks, metadata
# def load_text_chunks():
#     docs = []
#     for chunk_file in CHUNKS_DIR.glob("*.txt"):
#         text = chunk_file.read_text(encoding="utf-8").strip()
#         # docs.append(Document(page_content=text))
#         docs.append(Document(page_content=text, metadata={"source": str(chunk_file)}))

#     return docs




def load_text_chunks():
    docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)

    for chunk_file in CHUNKS_DIR.glob("*.txt"):
        text = chunk_file.read_text(encoding="utf-8").strip()
        # Split into smaller chunks
        split_chunks = splitter.split_text(text)

        for chunk_text in split_chunks:
            docs.append(Document(page_content=chunk_text, metadata={"source": str(chunk_file)}))

    return docs




def clear_old_chunks():
    for file in CHUNKS_DIR.glob("*.txt"):
        try:
            file.unlink()
            print(f"Deleted old chunk: {file.name}")
        except Exception as e:
            print(f"Failed to delete {file.name}: {e}")

def clear_index_dir():
    if FAISS_INDEX_DIR.exists() and FAISS_INDEX_DIR.is_dir():
        for item in FAISS_INDEX_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        print("Cleared all contents inside data/indexes.")
    else:
        print("Index directory does not exist.")

def build_and_save_faiss_index():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    

    docs = load_text_chunks()
    if not docs:
        raise ValueError("No documents found to build the FAISS index.")
    
    # Build FAISS index from docs
    faiss_index = FAISS.from_documents(docs, embedding_model)
    
    # Save the index locally
    faiss_index.save_local(str(INDEX_DIR / "faiss_index"))
    print(f"[INFO] FAISS index saved to {INDEX_DIR / 'faiss_index'}")

# def embed_chunks():
#     model = SentenceTransformer("all-MiniLM-L6-v2")

#     chunks, metadata = load_chunks()
#     embeddings = model.encode(chunks, show_progress_bar=True)
#     np.save(INDEX_DIR / "chunk_vectors.npy", embeddings)

#     with open(INDEX_DIR / "chunk_metadata.json", "w", encoding="utf-8") as f:
#         json.dump(metadata, f, indent=2)

#     print(f"[INFO] Saved {len(embeddings)} embeddings to {INDEX_DIR}")
