from transformers import pipeline
from link_to_text import link_to_FR

url = "https://www.elitigation.sg/gd/s/2018_SGCA_56"
text = link_to_FR(url)
summariser = pipeline("summarization") #default BART

summary = summariser(text, max_length=150, min_length=50, do_sample=False)
print(summary)
