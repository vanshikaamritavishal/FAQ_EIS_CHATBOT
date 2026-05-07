import os
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_embedding(text):
    return model.encode(text).tolist()

def get_embeddings(texts):
    return model.encode(texts).tolist()

def ask_llm(question, context):
    prompt = f"""
You are a helpful FAQ assistant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

Answer clearly:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content