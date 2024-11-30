import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class SentimentAnalyzer:
    def __init__(self):
        # Model name from HuggingFace (pre-trained for sentiment analysis)
        self.model_name = 'distilbert-base-uncased-finetuned-sst-2-english'
        
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        
    def analyze(self, text):
        # Convert text to model input format
        inputs = self.tokenizer(text, return_tensors='pt')
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Convert raw outputs to probabilities
        probabilities = torch.softmax(outputs.logits, dim=1)
        predicted_class = torch.argmax(probabilities).item()
        confidence = probabilities[0][predicted_class].item()
        
        # Convert numeric prediction to text label
        labels = ['Negative', 'Positive']
        return {
            "sentiment": labels[predicted_class],
            "confidence": round(confidence * 100, 2)
        }