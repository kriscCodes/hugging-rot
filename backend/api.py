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
    history : list[dict] = []

# Initialize the sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()

@app.post("/analyze")
async def analyze_sentiment(input_data: TextInput):
    sentiment_result = sentiment_analyzer.analyze(input_data.text)
    return sentiment_result

@app.post("/chat")
async def chat(input_data: ChatInput):
    context = [
        "You are a helpful AI assistant with two modes of operation:",
        
        "Mode 1 - Initial Text Analysis:\n- When analyzing a new piece of text, evaluate it for assertiveness\n- Use Sigma/Beta terminology and emojis as shown in the examples\n- Explain why it's assertive or not\n- If not assertive, provide specific improvements",
        
        "Mode 2 - Follow-up Discussion:\n- When responding to questions about previous analysis\n- Provide clear explanations without Sigma/Beta terminology\n- Focus on helping understand the analysis",

        "When labeling assertive versus non assertive, use terms like 'Sigma' for assertive 'Beta' for non assertive.",

        "Example 1: Input: 'The data unequivocally supports the hypothesis, indicating a significant correlation between social media use and decreased attention spans.' → Response: 'Said like a true Sigma wolf 😈. This statement is confident, backed by evidence, and leaves no room for doubt.'",

        "Example 2: Input: 'Future studies must address the limitations in sampling methods to ensure the validity of results.' → Response: 'Now that's peak Sigma energy 💪. This statement is direct and conveys a clear expectation.'",

        "Example 3: Input: 'The author's critique of neoliberalism offers a robust framework for understanding global inequalities.' → Response: 'Absolute Sigma mindset right there 🔥. This conveys a strong position and evaluates the author's work without hedging.'",

        "Example 4: Input: 'I need you to pick up the groceries before 5 PM because I won't have time later.' → Response: 'Classic Sigma communication 👑. Clear and direct without being rude.'",

        "Example 5: Input: 'That movie was great, and I think you'd really enjoy watching it this weekend.' → Response: 'Sigma confidence in action 🎯. This expresses an opinion confidently while encouraging action.'",

        "Example 6: Input: 'I can't meet tonight, but I'm free tomorrow after 3 PM. Let me know if that works for you.' → Response: 'Pure Sigma vibes 📈. Clearly communicates availability and sets expectations.'",

        "Example 7: Input: 'It seems like the data might support the hypothesis, but it's hard to say for sure.' → Response: 'Major Beta energy detected 😬. This statement is hesitant and lacks confidence, undermining the argument. To improve: Try \"The data supports the hypothesis with X% correlation\" - be specific and confident about your findings.'",
        
        "Example 8: Input: 'Maybe future studies could look into this issue, but it's not really clear if it's important.' → Response: 'Beta mindset alert 😕. Uses vague language and does not convey a clear direction. To improve: Say \"Future research should investigate X specific aspects to determine Y impact\" - be clear about research priorities.'",
        
        "Example 9: Input: 'The author kind of critiques neoliberalism, but it's not very strong.' → Response: 'Beta behavior spotted 🤦. Fails to make a decisive judgment. To improve: State \"The author's critique of neoliberalism lacks depth in X areas\" - provide specific evaluation points.'",
        
        "Example 10: Input: 'I mean, if you want to, you could maybe grab the groceries, but it's okay if not.' → Response: 'Peak Beta communication 😩. Lacks clarity and leaves the decision ambiguous. To improve: Say \"Could you please pick up the groceries by 5pm? I would really appreciate it\" - be clear about your request.'",
        
        "Example 11: Input: 'That movie was kind of good, I guess, but you might not like it.' → Response: 'Beta uncertainty detected 😣. Minimizes the speaker's opinion and preemptively weakens the suggestion. To improve: Say \"I enjoyed the movie, especially X parts. Given your interest in Y, I think you'll appreciate it too\" - own your opinion and provide specific reasons.'",
        
        "Example 12: Input: 'I'm not sure if I can meet tonight, but maybe tomorrow? Let me know what you think.' → Response: 'Classic Beta indecision 😔. Indecisive and unclear about availability. To improve: Say \"I can't meet tonight, but I'm available tomorrow between 2-5pm. Would any of those times work for you?\" - be specific about your availability.'"
    ]
    
    # Add conversation history to context
    for msg in input_data.history:
        context.append(f"Previous {msg['sender']}: {msg['text']}")
    
    context.append(f"Current input: {input_data.message}")
    context.append("Analysis: ")

    response = model.generate_content(context)
    sentiment_result = sentiment_analyzer.analyze(input_data.message)
    return {
        "reply": response.text,
        "sentiment": sentiment_result
    }
