from langchain_community.vectorstores import FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores.base import VectorStoreRetriever
# from app.core.utils.reranker import rerank_chunks
from langchain_core.retrievers import BaseRetriever

class RerankRetriever(BaseRetriever):
    def __init__(self, base_retriever, reranker_fn, top_k=5):
        self.base_retriever = base_retriever
        self.reranker_fn = reranker_fn
        self.top_k = top_k

    def _get_relevant_documents(self, query: str, **kwargs):
        docs = self.base_retriever.get_relevant_documents(query, **kwargs)
        return self.reranker_fn(query, docs, top_k=self.top_k)

def get_faiss_retriever():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    faiss_index = FAISS.load_local(
        "data/indexes/faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    retriever = faiss_index.as_retriever(search_kwargs={"k": 10})
    # return RerankRetriever(retriever)
    return faiss_index.as_retriever(search_kwargs={"k": 10})