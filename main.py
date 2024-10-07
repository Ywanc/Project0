from transformers import BartForConditionalGeneration, BartTokenizer
from utils import link_to_text
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)

model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn').to(device)
tokeniser = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

url = "https://www.elitigation.sg/gd/s/2018_SGCA_41"
text = link_to_text(url)

def summarise(text):
    inputs = tokeniser(text, return_tensors="pt", max_length=1024, truncation=True).to(device)
    summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=40, length_penalty=2.0, num_beams=3, early_stopping=True)
    return tokeniser.decode(summary_ids[0], skip_special_tokens=True)

print(text)
summary = summarise(text)
#print(f"original: {text}")
print(f"facts: {summary}")

