import os
import streamlit as st
from gpt4all import GPT4All
from huggingface_hub import hf_hub_download

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "Models_Files",
    "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
)

HF_REPO = "Tehreem786Irfan/BizBuddy-Mistral-Model"
HF_FILENAME = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"

def get_model_path():
    if os.path.exists(MODEL_PATH):
        print("🔵 Using LOCAL GGUF model")
        return MODEL_PATH
    else:
        print("🟣 Downloading model from HuggingFace Hub...")
        return hf_hub_download(repo_id=HF_REPO, filename=HF_FILENAME)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file does not exist: {MODEL_PATH!r}")

@st.cache_resource
def load_model():
    return GPT4All(MODEL_PATH, allow_download=False)

model = load_model()

def generate_business_advice(city, budget, interest):
    prompt = f"""
You are an AI Micro-Entrepreneur Coach. Give clear, concise advice.

City: {city}
Budget: {budget}
Interest: {interest}

Provide:
1. Three relevant business ideas.
2. A short 3-line startup plan for the best idea.
3. Two key profit drivers.
4. Two failure risks.
5. Two risk mitigation tips.
"""

    response = model.generate(
        prompt,
        max_tokens=150,
        temp=0.7,
        top_k=40,
        top_p=0.95,
        repeat_penalty=1.1,
        streaming=False
    )

    return response
