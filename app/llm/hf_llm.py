# from langchain.llms import HuggingFacePipeline
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login
import os
from dotenv import load_dotenv
import torch
# from llama_cpp import Llama
# from langchain.llms import LlamaCpp
from langchain_community.llms import LlamaCpp


load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
PHI_MINI_MODEL_PATH = "models/Phi-3-mini-4k-instruct-q4.gguf"  
MISTRAL_Q4_MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"



login(HUGGINGFACE_TOKEN)  
def get_Mistral_7B_llm():
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    # model_name = "HuggingFaceH4/zephyr-7b-beta"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        torch_dtype="auto"
        )


    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        do_sample=True,
    )

    return HuggingFacePipeline(pipeline=pipe)


def get_phi_mini_model_llm():
    llm= LlamaCpp(
        model_path=PHI_MINI_MODEL_PATH,
        n_ctx=4096,
        n_threads=8,  # Adjust based on CPU cores
        n_gpu_layers=0,  # Run entirely on CPU
        temperature=0.7,
        max_tokens=512
    )
    return llm

def get_mistral_7b_llm_quantized_4_bit():
    llm = LlamaCpp(
    model_path=MISTRAL_Q4_MODEL_PATH,  # You need this GGUF file
    n_gpu_layers=32,     # Run all on GPU
    n_threads=8,         # Max CPU threads
    use_mlock=True,      # Lock RAM for speed
    verbose=True,
    n_ctx=8192,                        # << Important: Set to 4096 or as per your model
    max_tokens=512 
    )
    return llm

