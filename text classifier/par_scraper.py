import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from urllib.parse import urljoin

# remove footnotes duh
def remove_footnotes(content):
    for sup in content.find_all('sup'): 
        sup.decompose()  
    for modal in content.find_all('div', class_=lambda x: x and "modal fade" in x):
        modal.decompose()
    #return content
    return " ".join(content.stripped_strings)

# remove paragraph number
def remove_num(text):
    return re.sub(r'^\d+\s+', '', text, flags=re.MULTILINE)

# mapping from header to label
def get_label(heading_text):
    label_mapping = {
    'facts': ['facts', 'background'],
    'decision': ['conclusion'],
    }
    for label, variations in label_mapping.items():
        if any(variation in heading_text.lower() for variation in variations):
            return label
    return None

# RETIRED INDEFINITELY
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
                cleaned_text = remove_num(remove_footnotes(sibling)).strip()
                if cleaned_text:
                    section_texts.append(cleaned_text)

            # group 3 paragraphs into 1 sample
            for i in range(0, len(section_texts), 3): 
                text = " ".join(section_texts[i:i+3]).strip()
                new_data = pd.DataFrame([[label, text]], columns=['label', 'text'])
                new_data.to_csv(file_path, mode='a', header=False, index=False)
    print("done")

# scraper for dataset. {text, label}
def scrape_to_csv(url, file_path, max_words_per_sample = 250):
    
    # find all main headings
    response = requests.get(url)
    print("url found")
    soup = BeautifulSoup(response.content, 'html.parser')
    print("scraping...")
    headings = soup.find_all(lambda tag:tag.name in ['div','p'], class_=lambda x:x and 'Judg-Heading-1' in x)
    print(f"number of headings: {len(headings)}")
    
    # for each heading
    for head in headings:
        label = get_label(head.text.lower())
        section_texts = []
        
        # label it: 'facts', 'ruling', 'others'
        if label: 
            print(f"found {label}, {head.text}")
        else: 
            label = 'others'
            
        # collect text until reach wordcount, next header or the end
        curr_wordcount=0
        for sibling in head.find_next_siblings():
            if sibling.has_attr('class') and any('Judg-Heading-1' in x for x in sibling['class']): #if reach next header, stop
                break
            if sibling.has_attr('class') and any('Judg-Heading' in x for x in sibling['class']): # skip subheader
                continue
            text = remove_num(remove_footnotes(sibling)).strip()
            curr_wordcount+=len(text.split())
            if curr_wordcount > max_words_per_sample: #if adding this paragraph will exceed 250 words, don't
                break
            section_texts.append(text)
                
        text = " ".join(section_texts).strip()
        
        # 
        if text:
            new_data = pd.DataFrame([[url.split('/')[-1], label, len(text.split()), text]], columns=['case_number', 'label', 'word_count', 'text'])
            new_data.to_csv(file_path, mode='a', header=False, index=False)
    print("done")

# fetch all case links from a page
def fetch_case_links(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all('a', class_='gd-heardertext')
    case_links = [urljoin(base_url, tag.get("href")) for tag in tags]
    return case_links

url1 = "https://www.elitigation.sg/gd/Home/Index?Filter=SUPCT&YearOfDecision=All&SortBy=DateOfDecision&CurrentPage=" 
url2 = "&SortAscending=False&PageSize=0&Verbose=False&SearchQueryTime=0&SearchTotalHits=0&SearchMode=True&SpanMultiplePages=False"
for i in range(1, 500):
    links = fetch_case_links(url1 + str(i) + url2)
    print(f"\nSCRAPING {i}th page...\n")
    for link in links:
        scrape_to_csv(link, "dataset.csv")