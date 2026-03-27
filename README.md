# FastAPI Gemini Chatbot

A lightweight chatbot app using FastAPI for the backend and Gemini Pro for responses.

## 1) Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment:

```bash
cp .env.example .env
```

Edit `.env` and set your Google API key.

## 2) Run

```bash
uvicorn app:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 3) API

- `POST /chat`
  - Request JSON: `{ "message": "Hello" }`
  - Response JSON: `{ "reply": "..." }`
