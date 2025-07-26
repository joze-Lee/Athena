from langchain_community.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.base import VectorStoreRetriever
# from app.core.utils.reranker import rerank_chunks
from langchain_core.retrievers import BaseRetriever

# MODEL_NAME="BAAI/bge-base-en-v1.5"
MODEL_NAME="all-MiniLM-L6-v2"


def get_faiss_retriever():
    embedding_model = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    faiss_index = FAISS.load_local(
        "data/indexes/faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    retriever = faiss_index.as_retriever(search_kwargs={"k": 20})
    return  retriever
    
    
