import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# ===== INTERNAL IMPORTS =====
from app.core.system_prompt import COMPANY_SYSTEM_PROMPT
from app.agents.supervisor import route_task
from app.agents.chat_agent import chat_agent
from app.agents.build_agent import build_agent
from app.agents.research_agent import research_agent
from app.agents.file_agent import file_agent

# ===== CONFIG =====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ===== FASTAPI APP =====
app = FastAPI(
    title="Origin AI by Origin",
    description="Cypher — multi-agent AI system",
    version="1.0.0"
)

# ===== REQUEST MODEL =====
class ChatRequest(BaseModel):
    message: str
    file_content: Optional[str] = None  # for future file uploads

# ===== HEALTH CHECK =====
@app.get("/")
def root():
    return {
        "message": "ask anything"
    }

# ===== PRIMARY GEMINI CALL =====
def call_gemini(prompt: str):
    response = model.generate_content(prompt)
    return response.text

# ===== SAFE FALLBACK =====
def fallback_response(user_input: str):
    return f"""
Cypher (fallback mode):

I'm experiencing a temporary issue with the main intelligence system.

Here’s a quick response based on your request:
{user_input}

Please try again shortly for a more detailed answer.
"""

# ===== CHAT ENDPOINT =====
@app.post("/chat")
def chat(req: ChatRequest):
    task = route_task(req.message)

    try:
        # ===== AGENT ROUTING =====
        if task == "build":
            result = build_agent(model, COMPANY_SYSTEM_PROMPT, req.message)

        elif task == "research":
            result = research_agent(model, COMPANY_SYSTEM_PROMPT, req.message)

        elif task == "file":
            result = file_agent(
                model,
                COMPANY_SYSTEM_PROMPT,
                req.message,
                req.file_content or ""
            )

        else:
            result = chat_agent(model, COMPANY_SYSTEM_PROMPT, req.message)

        # ===== BASIC VALIDATION =====
        if not result or len(result.strip()) == 0:
            raise ValueError("Empty response from model")

        return {
            "status": "success",
            "agent": task,
            "response": result
        }

    except Exception as e:
        print("Primary system failed:", str(e))

        try:
            # ===== FALLBACK =====
            fallback = fallback_response(req.message)

            return {
                "status": "fallback",
                "agent": "fallback",
                "response": fallback
            }

        except Exception as fallback_error:
            print("Fallback failed:", str(fallback_error))

            return {
                "status": "error",
                "response": "Cypher is temporarily unavailable. Please try again shortly."
            }
