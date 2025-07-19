# athena/app/core/pdf_parser.py

import fitz  # PyMuPDF
import os
import re
from pathlib import Path
import logging
from nltk.tokenize import sent_tokenize

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

TARGET_CHUNK_SIZE = 350  # character count target (~300–400)

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        logging.error(f"Failed to open {pdf_path}: {e}")
        return ""

    text = ""
    for page_num, page in enumerate(doc, 1):
        page_text = page.get_text()
        if not page_text.strip():
            logging.warning(f"Page {page_num} in {pdf_path} has no extractable text.")
        text += page_text
    doc.close()
    return text

def clean_text(text):
    # Remove extra whitespace, newlines, special characters
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text.strip()

def chunk_text_by_sentences(text, target_chunk_size=TARGET_CHUNK_SIZE, max_sentences=3):
    sentences = sent_tokenize(text)
    chunks = []

    current_chunk = []
    current_len = 0

    for sent in sentences:
        if len(current_chunk) >= max_sentences or current_len + len(sent) > target_chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk).strip())
                current_chunk = []
                current_len = 0
        current_chunk.append(sent)
        current_len += len(sent)

    # Add the final leftover chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk).strip())

    return chunks

def process_pdf(pdf_path, chunk_output_dir):
    logging.info(f"Processing {pdf_path}")

    text = extract_text_from_pdf(pdf_path)
    if not text:
        logging.error(f"No text extracted from {pdf_path}. Skipping chunking.")
        return None

    cleaned = clean_text(text)
    chunks = chunk_text_by_sentences(cleaned)  # ✅ NEW chunking method

    pdf_name = Path(pdf_path).stem
    chunk_dir = Path(chunk_output_dir)
    chunk_dir.mkdir(parents=True, exist_ok=True)

    chunk_paths = []
    for idx, chunk in enumerate(chunks):
        chunk_file = chunk_dir / f"{pdf_name}_chunk{idx}.txt"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        chunk_paths.append(str(chunk_file))

    logging.info(f"Saved {len(chunks)} chunks from {pdf_name}")

    return {
        "pdf_name": pdf_name,
        "num_chunks": len(chunks),
        "chunk_paths": chunk_paths
    }
