from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import get_embedding, get_embeddings, ask_llm
from faiss_store import VectorStore
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
store = None

class Question(BaseModel):
    question: str

@app.on_event("startup")
def load_data():
    global store

    with open("../data/faq.txt", "r", encoding="utf-8") as f:
        texts = f.read().split("\n\n")

    embeddings = get_embeddings(texts)

    store = VectorStore(len(embeddings[0]))
    store.add(embeddings, texts)

@app.post("/ask")
def ask(q: Question):
    query_emb = get_embedding(q.question)

    relevant_docs = store.search(query_emb, k=3)
    context = "\n".join(relevant_docs)

    answer = ask_llm(q.question, context)

    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)