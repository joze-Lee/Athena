# from huggingface_hub import InferenceClient
# import os
# from dotenv import load_dotenv
# load_dotenv()

# HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# client = InferenceClient(token=HUGGINGFACE_TOKEN)


# response = client.text_generation(
#     "Your input text here",  # directly pass input string or list of strings as the first argument
#     model="mistralai/Mistral-7B-Instruct-v0.2",
#     parameters={"max_new_tokens": 512}
# )

# print(response)
from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    n_gpu_layers=-1,  # All on GPU via Metal
    n_threads=8,
    use_mlock=True,
    verbose=True,
    max_tokens=512,   # adjust as needed
    temperature=0.7
)

response = llm("Explain Apple Metal acceleration in one sentence.")
print(response)
