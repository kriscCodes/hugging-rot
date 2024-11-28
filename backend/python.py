import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Model name from HuggingFace (pre-trained for sentiment analysis)
model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Load model with memory optimizations:
# - torch_dtype=torch.float16: Use 16-bit precision instead of 32-bit (saves memory)
# - low_cpu_mem_usage=True: More memory-efficient loading
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)

# Example text to analyze
text = "I absolutely hated the movie! It was terrible."

# Convert text to model input format
inputs = tokenizer(text, return_tensors='pt')

# Make prediction
# torch.no_grad() tells PyTorch not to track gradients (saves memory)
with torch.no_grad():
    outputs = model(**inputs)

# Convert raw outputs to probabilities between 0 and 1
probabilities = torch.softmax(outputs.logits, dim=1)

# Get the highest probability class
predicted_class = torch.argmax(probabilities).item()

# Convert numeric prediction to text label
labels = ['Negative', 'Positive']
print(f"Predicted sentiment: {labels[predicted_class]}")