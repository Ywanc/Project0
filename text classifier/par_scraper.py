import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv

def remove_footnotes(content):
    for sup in content.find_all('sup'): 
        sup.decompose()  
    for modal in content.find_all('div', class_=lambda x: x and "modal fade" in x):
        modal.decompose()
    return " ".join(content.stripped_strings)

def remove_num(text):
    return re.sub(r'^\d+\s+', '', text, flags=re.MULTILINE)

def get_label(heading_text):
    label_mapping = {
    'facts': ['facts', 'background', 'introduction'],
    'decision': ['decision', 'judgment', 'ruling', 'outcome', 'conclusion'],
    'rationale': ['rationale', 'reasoning', 'justification', 'grounds']
    }
    for label, variations in label_mapping.items():
        if any(variation in heading_text.lower() for variation in variations):
            return label
    return None

# UNDER CONSTRUCTION
def scrape_sections_to_csv(url, file_path):
    response = requests.get(url)
    print("url found")
    soup = BeautifulSoup(response.content, 'html.parser')
    print("scraping...")
    # find all headings
    headings = soup.find_all(lambda tag:tag.name in ['div','p'], class_=lambda x:x and 'Judg-Heading' in x)
    print(f"number of headings: {len(headings)}")
    # for each heading
    for head in headings:
        section_texts = []
        label = get_label(head.text.lower())
        
        # if label exists, then get all the following paragraphs after the header
        if label: 
            print(f"found {label}, {head.text}")
            for sibling in head.find_next_siblings():
                print(sibling)
                if (sibling.name == 'div' or sibling.name=='p') and (sibling.has_attr('class') and 'Judg-Heading' in sibling["class"][0]): #stop if reach another header 
                    break
                cleaned_text = remove_num(remove_footnotes(sibling).strip())
                if cleaned_text:
                    section_texts.append(cleaned_text)

            # group 3 paragraphs into 1 sample
            for i in range(0, len(section_texts), 3): 
                text = " ".join(section_texts[i:i+3]).strip()
                new_data = pd.DataFrame([[label, text]], columns=['label', 'text'])
                new_data.to_csv(file_path, mode='a', header=False, index=False)
    print("done")

# only scrapes 1st paragraph for each section
def scrape1(url, file_path, words_per_sample=3):
    response = requests.get(url)
    print("url found")
    soup = BeautifulSoup(response.content, 'html.parser')
    print("scraping...")
    # find all headings
    headings = soup.find_all(lambda tag:tag.name in ['div','p'], class_=lambda x:x and 'Judg-Heading' in x)
    print(f"number of headings: {len(headings)}")
    # for each heading
    for head in headings:
        label = get_label(head.text.lower())
        section_texts = []
        # if label exists, then get all the following paragraphs after the header
        if label: 
            print(f"found {label}, {head.text}")
            curr_wordcount, i = 0, 0
            while curr_wordcount < 100 and head.find_next_siblings()[i]: # need early stopping condition if hit end/another header
                sibling = head.find_next_siblings()[i]
                text = remove_num(remove_footnotes(sibling)).strip()
                section_texts.append(text)
                curr_wordcount+=len(text)
                i+=1
            '''for i in range(0, par_per_sample+1):
                sibling = head.find_next_siblings()[i]
                text = remove_num(remove_footnotes(sibling)).strip()
                section_texts.append(text)'''
            text = " ".join(section_texts)
            if text:
                new_data = pd.DataFrame([[url.split('/')[-1], label, text]], columns=['case_number', 'label', 'text'])
                new_data.to_csv(file_path, mode='a', header=False, index=False)
    print("done")
    
url = "https://www.elitigation.sg/gd/s/2015_SGHC_125"
scrape1(url, "dataset.csv")

#df = pd.DataFrame(columns = ['text', 'label'])
#new_sample = pd.DataFrame({'text': [text], 'label': ['facts']})
#df = pd.concat([df, new_sample], ignore_index = True)

# Save the updated DataFrame to CSV
#df.to_csv('dataset.csv', index=False)