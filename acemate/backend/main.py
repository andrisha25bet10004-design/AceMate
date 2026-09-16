from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
import ollama

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "AceMate backend is running!"}


@app.post("/chat")
def chat(request: ChatRequest):

    # Primary: Gemini
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=request.message
        )

        return {
            "reply": response.text,
            "model": "gemini-3.6-flash"
        }

    # Fallback: Ollama
    except Exception as error:
        print(f"Gemini failed: {error}")

        try:
            response = ollama.chat(
                model="phi3:latest",
                messages=[
                    {
                        "role": "user",
                        "content": request.message
                    }
                ]
            )

            return {
                "reply": response["message"]["content"],
                "model": "phi3:latest"
            }

        except Exception as ollama_error:
            print(f"Ollama failed: {ollama_error}")

            return {
                "reply": "Sorry, AceMate is temporarily unable to generate a response."
            }