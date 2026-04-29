import os
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from app.core.system_prompt import COMPANY_SYSTEM_PROMPT

# ===== CONFIG =====
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

app = FastAPI(title="Origin AI by Origin")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "message": "ask anything"
    }

# ===== PRIMARY MODEL =====
def call_gemini(prompt: str):
    response = model.generate_content(prompt)
    return response.text

# ===== FALLBACK MODEL =====
def fallback_response(user_input: str):
    return f"""
Cypher (fallback mode):

I’m currently experiencing high load or a temporary issue with the main AI system.

Here’s a quick response based on your request:

{user_input}

Please try again shortly for a more detailed answer.
"""

# ===== CHAT ENDPOINT =====
@app.post("/chat")
def chat(req: ChatRequest):
    full_prompt = f"""
{COMPANY_SYSTEM_PROMPT}

USER:
{req.message}
"""

    try:
        # 🔥 PRIMARY (Gemini)
        result = call_gemini(full_prompt)
        return {"response": result}

    except Exception as e:
        print("Gemini failed:", str(e))

        try:
            # 🔁 FALLBACK
            result = fallback_response(req.message)
            return {"response": result}

        except Exception as fallback_error:
            print("Fallback failed:", str(fallback_error))

            return {
                "response": "Cypher is temporarily unavailable. Please try again shortly."
            }
