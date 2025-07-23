from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Health check route
@app.get("/")
async def root():
    return {"message": "✅ Zaffy backend running successfully."}

# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Chat endpoint
@app.post("/chat")
async def chat_with_zaffy(chat: ChatRequest):
    hf_api_key = os.getenv("HF_API_KEY")
    hf_model = "Qwen/Qwen1.5-0.5B-Chat"
    api_url = f"https://api-inference.huggingface.co/models/{hf_model}"

    headers = {
        "Authorization": f"Bearer {hf_api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"<|user|>\n{chat.message}\n<|assistant|>"

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        result = response.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            full_text = result[0]["generated_text"]
            reply = full_text.split("<|assistant|>")[-1].strip()
        else:
            reply = "Zaffy couldn’t understand that. Try again?"

    except Exception as e:
        reply = "Zaffy encountered an error while responding."

    return {
        "user_id": chat.user_id,
        "message": chat.message,
        "reply": reply,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
