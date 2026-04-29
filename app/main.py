import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from app.core.system_prompt import COMPANY_SYSTEM_PROMPT

# ===== CONFIG =====
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="Origin AI by Origin")

# ===== REQUEST MODEL =====
class ChatRequest(BaseModel):
    message: str

# ===== ROOT =====
@app.get("/")
def root():
    return {
        "message": "ask anything"
    }

# ===== CHAT =====
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        full_prompt = f"""
{COMPANY_SYSTEM_PROMPT}

USER:
{req.message}
"""

        response = model.generate_content(full_prompt)

        return {
            "response": response.text
        }

    except Exception as e:
        return {
            "response": f"Error: {str(e)}"
        }
