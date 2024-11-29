import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentiment_analyzer import SentimentAnalyzer  # Import the sentiment analyzer

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Correct origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment.")
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
)

class TextInput(BaseModel):
    text: str

class ChatInput(BaseModel):
    message: str

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()

@app.post("/analyze")
async def analyze_sentiment(input_data: TextInput):
    sentiment_result = sentiment_analyzer.analyze(input_data.text)
    return sentiment_result

@app.post("/chat")
async def chat(input_data: ChatInput):
    response = model.generate_content([
        f"input: {input_data.message}",
        "output: ",
    ])
    sentiment_result = sentiment_analyzer.analyze(input_data.message)
    return {
        "reply": response.text,
        "sentiment": sentiment_result
    }