from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
from pydantic import BaseModel
import shutil
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.utils.s3 import upload_pdf_to_s3
from app.core.utils.pdf_parser import process_pdf
from app.core.utils.embedder import embed_chunks
from app.core.utils.faiss_indexer import build_faiss_index,search
from app.core.utils.reranker import rerank_chunks


router = APIRouter()
model = SentenceTransformer("all-MiniLM-L6-v2")

CHUNKS_DIR = Path("data/chunks")
UPLOAD_DIR = Path("data/pdfs")


# ---------------------------
# Upload PDF Route
# ---------------------------

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    success = upload_pdf_to_s3(file.file, file.filename)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to upload file.")
    
    process_pdf(file_path, CHUNKS_DIR)
    embed_chunks()
    build_faiss_index()
    
    return {"message": "Upload successful", "filename": file.filename}





# ---------------------------
# Query Route
# ---------------------------

class QueryInput(BaseModel):
    query: str


@router.post("/query")
async def ask_question(input: QueryInput):
    q_vec = model.encode([input.query])
    q_vec = q_vec / np.linalg.norm(q_vec, axis=1, keepdims=True)

    results, scores = search(q_vec, top_k=10)
    top_chunks = [{"text": r["text"], "score": s} for r, s in zip(results, scores)]
    reranked = rerank_chunks(input.query, top_chunks, top_k=5)

    return {"results": reranked}