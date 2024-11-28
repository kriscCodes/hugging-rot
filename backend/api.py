from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from python import SentimentAnalyzer

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model
analyzer = SentimentAnalyzer()

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_sentiment(input_data: TextInput):
    return analyzer.analyze(input_data.text)