import random
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Minimal Typing Test API",
    description="A simple FastAPI backend that returns quotes and calculates typing stats."
)

# CORS middleware enables your frontend (like a React or vanilla JS web app)
# to communicate with this backend when running locally.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Hardcoded quotes to start with
QUOTES = [
    {"id": 1, "text": "The quick brown fox jumps over the lazy dog.", "author": "Anonymous"},
    {"id": 2, "text": "Talk is cheap. Show me the code.", "author": "Linus Torvalds"},
    {"id": 3, "text": "Simplicity is the soul of efficiency.", "author": "Austin Freeman"},
    {"id": 4, "text": "First, solve the problem. Then, write the code.", "author": "John Johnson"},
    {"id": 5, "text": "Programs must be written for people to read, and only secondarily for machines to execute.", "author": "Harold Abelson"},
    {"id": 6, "text": "One of my most productive days was throwing away 1000 lines of code.", "author": "Ken Thompson"},
    {"id": 7, "text": "Make it work, make it right, make it fast.", "author": "Kent Beck"}
]

# Request payload for submitting typing results
class SubmitTestPayload(BaseModel):
    original_text: str = Field(..., description="The quote that the user was asked to type")
    typed_text: str = Field(..., description="The actual text the user typed")
    time_taken_seconds: float = Field(..., gt=0, description="Time elapsed in seconds")

@app.get("/")
def home():
    return {
        "message": "Welcome to the typing test backend!",
        "endpoints": {
            "get_random_quote": "GET /quote",
            "submit_typing_test": "POST /submit"
        }
    }

@app.get("/quote")
def get_random_quote():
    """Returns a random quote for the user to type."""
    if not QUOTES:
        raise HTTPException(status_code=500, detail="No quotes available.")
    return random.choice(QUOTES)

@app.post("/submit")
def submit_test(payload: SubmitTestPayload):
    """
    Receives what the user typed and how long they took,
    calculates their WPM and accuracy, and returns the stats.
    """
    # Count matching characters character-by-character
    correct_chars = sum(1 for o, t in zip(payload.original_text, payload.typed_text) if o == t)
    
    # 1. WPM calculation
    # Standard formula: (correct_chars / 5) / (seconds / 60)
    wpm = (correct_chars / 5.0) / (payload.time_taken_seconds / 60.0)
    
    # 2. Accuracy calculation
    # Compare correct matching characters to the max length of both strings.
    # This penalizes both typos (incorrect characters) and typing too few/many characters.
    max_length = max(len(payload.original_text), len(payload.typed_text))
    accuracy = (correct_chars / max_length) * 100.0 if max_length > 0 else 0.0
    
    return {
        "wpm": round(wpm, 2),
        "accuracy": round(accuracy, 2),
        "correct_characters": correct_chars,
        "total_characters": len(payload.original_text),
        "time_taken_seconds": payload.time_taken_seconds
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
