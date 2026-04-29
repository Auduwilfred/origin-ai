from fastapi import FastAPI
from pydantic import BaseModel
from app.core.system_prompt import COMPANY_SYSTEM_PROMPT

app = FastAPI(title="Origin AI by Origin")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "message": "ask anything"
    }

@app.post("/chat")
def chat(req: ChatRequest):
    full_prompt = f"""
{COMPANY_SYSTEM_PROMPT}

USER:
{req.message}
"""

    # TEMP RESPONSE (next step = Gemini)
    return {
        "response": f"Cypher:\n\n{req.message}"
    }
