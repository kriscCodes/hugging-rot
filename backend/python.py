import transformers
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

# Replace the model name with the one you've chosen
model_name = 'distilbert-base-uncased-finetuned-sst-2-english'

# Load the tokenizer
tokenizer = DistilBertTokenizer.from_pretrained(model_name)

# Load the pre-trained and fine-tuned model
model = DistilBertForSequenceClassification.from_pretrained(model_name)

# Sample text
text = "I absolutely hated the movie! It was terrible."

# Tokenize the input text
inputs = tokenizer(text, return_tensors='pt')  # 'pt' for PyTorch tensors

# Get model outputs
outputs = model(**inputs)

# Extract logits (raw predictions)
logits = outputs.logits

# Convert logits to probabilities (optional)
probabilities = torch.softmax(logits, dim=1)

# Get the predicted class
predicted_class = torch.argmax(probabilities).item()

# Map the predicted class to its label
labels = ['Negative', 'Positive']
print(f"Predicted sentiment: {labels[predicted_class]}")