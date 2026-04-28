from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Origin AI by Origin")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Hello, I'm Origin AI — Origin's central intelligence. How can I help build the future today?"}

@app.post("/chat")
def chat(req: ChatRequest):
    return {
        "response": f"Origin AI received: {req.message}"
    }
