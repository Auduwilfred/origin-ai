import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from app.core.system_prompt import COMPANY_SYSTEM_PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
model = genai.GenerativeModel(MODEL)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    tool: str = "Normal Chat"

# ===== TOOL HANDLERS =====

def code_generator(prompt):
    return model.generate_content(
        f"{COMPANY_SYSTEM_PROMPT}\n\nGenerate production-grade code:\n{prompt}"
    ).text

def thinking_mode(prompt):
    return model.generate_content(
        f"{COMPANY_SYSTEM_PROMPT}\n\nThink step-by-step deeply:\n{prompt}"
    ).text

def web_search(prompt):
    return model.generate_content(
        f"{COMPANY_SYSTEM_PROMPT}\n\nSearch and summarize latest info:\n{prompt}"
    ).text

def normal_chat(prompt):
    return model.generate_content(
        f"{COMPANY_SYSTEM_PROMPT}\n\nUser:\n{prompt}"
    ).text

# ===== ROUTER =====
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        if req.tool == "Code Generator":
            result = code_generator(req.message)

        elif req.tool == "Thinking Mode":
            result = thinking_mode(req.message)

        elif req.tool == "Web Search":
            result = web_search(req.message)

        else:
            result = normal_chat(req.message)

        return {"response": result}

    except Exception as e:
        return {"response": f"Error: {str(e)}"}
