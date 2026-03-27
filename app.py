import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not GOOGLE_API_KEY:
    raise RuntimeError(
        "Missing GOOGLE_API_KEY. Copy .env.example to .env and set your key."
    )

client = genai.Client(api_key = GOOGLE_API_KEY)

app = FastAPI(title="Gemini FastAPI Chatbot")
app.mount("/static", StaticFiles(directory="static"), name="static")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    print(client.models.list())
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    user_message = payload.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_message
        )
        reply_text = (response.text or "").strip()
        if not reply_text:
            reply_text = "I could not generate a response this time."
        return ChatResponse(reply=reply_text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini request failed: {exc}")
