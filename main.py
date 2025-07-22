from fastapi import FastAPI, Request
from pydantic import BaseModel
import datetime

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat_endpoint(chat: ChatRequest):
    user_message = chat.message
    # Placeholder for Qwen response (to be added)
    bot_reply = "Zaffy will reply soon..."
    
    # Timestamp logging
    log = {
        "user_id": chat.user_id,
        "message": user_message,
        "reply": bot_reply,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # [🔜Future] Upload this log to Backblaze
    return log
