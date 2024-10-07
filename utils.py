import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def remove_footnotes(content):
    for sup in content.find_all('sup'): 
        sup.decompose()  
    for modal in content.find_all('div', class_=lambda x: x and "modal fade" in x):
        modal.decompose()
    return " ".join(content.stripped_strings)

def remove_num(text):
    return re.sub(r'^\d+\s+', '', text, flags=re.MULTILINE)

def link_to_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        headings = soup.find_all('div', class_=lambda x: x and "Judg-Heading" in x)
        all_para = []
        
        keywords = ["facts", "fact", "background"]
        for head in headings:
            if any(keyword in head.text.lower() for keyword in keywords):
                for sibling in head.find_next_siblings(): #for each sibling
                    if sibling.name == 'div' and 'Judg-Heading' in sibling["class"][0]:
                        break
                    sibling = remove_footnotes(sibling)
                    cleaned_text = remove_num(sibling.strip())
                    if cleaned_text:
                        all_para.append(cleaned_text)

        # Join all paragraphs into one text block
        text = " ".join(all_para)
        print(text)
        return text
        
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        
