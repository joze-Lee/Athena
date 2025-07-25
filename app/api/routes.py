from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
from pydantic import BaseModel
import shutil
# import numpy as np
# from sentence_transformers import SentenceTransformer
from functools import lru_cache

from app.qa_pipeline.langchain_pipeline import generate_answer_with_context
from app.core.utils.s3 import upload_pdf_to_s3
from app.core.utils.pdf_parser import process_pdf
from app.core.utils.embedder import build_and_save_faiss_index #, embed_chunks
# from app.core.utils.faiss_indexer import build_faiss_index,search
from app.core.utils.reranker import rerank_chunks
from app.qa_pipeline.langchain_pipeline import get_langchain_qa_pipeline  # NEW IMPORT

router = APIRouter()
# model = SentenceTransformer("all-MiniLM-L6-v2")

CHUNKS_DIR = Path("data/chunks")
UPLOAD_DIR = Path("data/pdfs")


@lru_cache(maxsize=1)
def get_cached_pipeline():
    return get_langchain_qa_pipeline()


# ---------------------------
# Upload PDF Route
# ---------------------------

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = UPLOAD_DIR / file.filename

    # Save to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Reset file pointer to start before uploading to S3
    file.file.seek(0)
    success = upload_pdf_to_s3(file.file, file.filename)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload file.")
    
    process_pdf(file_path, CHUNKS_DIR)
    # embed_chunks()
    build_and_save_faiss_index()
    # build_faiss_index()
    
    return {"message": "Upload successful", "filename": file.filename}





# ---------------------------
# Query Route
# ---------------------------

class QueryInput(BaseModel):
    query: str


# @router.post("/query")
# async def ask_question(input: QueryInput):
#     q_vec = model.encode([input.query])
#     q_vec = q_vec / np.linalg.norm(q_vec, axis=1, keepdims=True)

#     results, scores = search(q_vec, top_k=10)
#     top_chunks = [{"text": r["text"], "score": s} for r, s in zip(results, scores)]
#     reranked = rerank_chunks(input.query, top_chunks, top_k=5)

#     return {"results": reranked}


# ----------------------------------
# Query Route (UPDATED to LangChain)
# ----------------------------------

@router.post("/query")
async def ask_question(input: QueryInput):
    qa_pipeline = get_cached_pipeline()
    
    # Run the query through the QA pipeline
    result = qa_pipeline.invoke({"query": input.query})

    # Extract source documents from the result
    source_docs = result["source_documents"]
    top_chunks = [{"text": doc.page_content, "score": None} for doc in source_docs]

    # Optional: Rerank the top chunks (you could directly return the result instead if reranking is unnecessary)
    reranked = rerank_chunks(input.query, top_chunks, top_k=5)
    
    generated_answer = generate_answer_with_context(reranked, input.query)

    # generated_answer = generate_answer_with_context(reranked, input.query)
    
    return {
    "results": reranked,
    "answer": generated_answer
    }
    # return {"results": reranked}
