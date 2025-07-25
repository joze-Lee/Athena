from langchain.chains import RetrievalQA
from app.llm.hf_llm import get_huggingface_llm
from app.llm.prompt_templates import get_default_prompt,get_generation_prompt
from app.retriever.retriever import get_faiss_retriever
from functools import lru_cache

NUM_CONTEXT_CHUNKS = 3

@lru_cache(maxsize=1)
def get_cached_huggingface_llm():
    return get_huggingface_llm()


def get_langchain_qa_pipeline():
    llm = get_cached_huggingface_llm()
    retriever = get_faiss_retriever()
    prompt = get_default_prompt()

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )


# Prepare context by joining chunk texts
def prepare_context(chunks: list[dict]) -> str:
    return "\n\n".join(chunk["text"] for chunk in chunks)

# New function to generate answer using your LLM pipeline
def generate_answer_with_context( chunks: list[dict], question: str) -> str:
    
    limited_chunks = chunks[:NUM_CONTEXT_CHUNKS]
    context = prepare_context(limited_chunks)
    prompt = get_generation_prompt(context, question)
    llm = get_cached_huggingface_llm()
    # Generate text using HuggingFacePipeline's __call__
    generated_text = llm(prompt)
    
    # # Sometimes output repeats prompt — strip it if needed
    # if generated_text.startswith(prompt):
    #     return generated_text[len(prompt):].strip()
    # else:
    #     return generated_text.strip()
    
    # If output is a list (some pipeline versions), extract text
    print("irungaaa bhai....................... : "+generated_text)
    if isinstance(generated_text, list) and "generated_text" in generated_text[0]:
        generated_text = generated_text[0]["generated_text"]
    print("mudichitinga ponga............ : "+generated_text)
    # Post-process to extract clean answer
    answer_start = generated_text.find("Answer:") + len("Answer:")
    print("INdex vlaue  ", answer_start)
    clean_answer = generated_text[answer_start:].strip()
    print("cleaned answer : " , clean_answer)
    return clean_answer
