from langchain.prompts import PromptTemplate

def get_default_prompt():
    return PromptTemplate.from_template(
        """You are Athena, an expert AI assistant. Answer the question based only on the context.

        Context:
        {context}

        Question: {question}
        Answer concisely:"""
    )

def get_generation_prompt(context: str, question: str) -> str:
    return f"""You are a helpful assistant. Answer the question based ONLY on the context provided. 
If the answer cannot be found in the context, say "I don't know".

Context:
{context}

Question: {question}
Answer:"""