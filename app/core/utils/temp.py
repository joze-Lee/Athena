from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

client = InferenceClient(token=HUGGINGFACE_TOKEN)


response = client.text_generation(
    "Your input text here",  # directly pass input string or list of strings as the first argument
    model="mistralai/Mistral-7B-Instruct-v0.2",
    parameters={"max_new_tokens": 512}
)

print(response)
