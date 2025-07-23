from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file (locally)
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Hugging Face credentials from env
HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")
MODEL_ID = "Qwen/Qwen1.5-0.5B-Chat"  # Change to larger free model if needed

# Request format
class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat(chat: ChatRequest):
    prompt = f"User: {chat.message}\nAssistant:"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200,
            "return_full_text": False
        }
    }

    try:
        res = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_ID}",
            headers=headers,
            json=payload
        )
        if res.status_code == 200:
            output = res.json()
            reply = output[0]["generated_text"].strip()
        else:
            reply = f"Zaffy is facing issues. HF response: {res.status_code}"

    except Exception as e:
        reply = f"Server error: {str(e)}"

    return {
        "user_id": chat.user_id,
        "message": chat.message,
        "reply": reply,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
