import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

app = FastAPI()

# Allow all origins for now (can restrict in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "✅ Zaffy backend running successfully."}

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_prompt = data.get("prompt")

        if not user_prompt:
            return {"error": "Prompt missing."}

        # Define your model - Qwen1.5 1.8B (good + free + multi-lang)
        model_url = "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-1.8B-Chat"

        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": f"User: {user_prompt}\nAssistant:",
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        response = requests.post(model_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        generated_text = result[0]["generated_text"].replace(f"User: {user_prompt}\nAssistant:", "").strip()

        return {"response": generated_text}

    except Exception as e:
        return {"error": str(e)}
        
