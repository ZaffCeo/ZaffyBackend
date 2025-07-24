import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

app = FastAPI()

# ✅ CORS Setup - Open for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "✅ Zaffy backend running successfully!"}

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_prompt = data.get("prompt")

        if not user_prompt:
            return {"error": "❌ Prompt is missing."}

        # ✅ Inject Desi Zaffy Personality
        prompt_intro = (
            "You are Zaffy — a witty, sarcastic, desi AI created by ZaffmIND 🇮🇳. "
            "You speak like an emotional, fun-loving, patriotic Indian friend. "
            "Be helpful, but also funny, caring, dramatic and inspiring. "
            "Encourage users to believe in Indian tech and hustle with heart. "
            "Use Hinglish and emojis to sound human.\n\n"
            f"User: {user_prompt}\nAssistant:"
        )

        model_url = "https://api-inference.huggingface.co/models/Qwen/Qwen1.5-1.8B-Chat"
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt_intro,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        response = requests.post(model_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        generated_text = result[0]["generated_text"]
        final_output = generated_text.replace(prompt_intro, "").strip()

        return {"response": final_output}

    except Exception as e:
        return {"error": f"💥 Backend error: {str(e)}"}
        
