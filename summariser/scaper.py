import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# takes in url and get the judgement text
def link_to_text(url,case_id,output_dir):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', id='divJudgement')
        
        #remove the footnotes
        for sup in content.find_all('sup'): 
            sup.decompose()  
        for modal in content.find_all('div', class_=lambda x: x and "modal fade" in x):
            modal.decompose()  
        
        filename = os.path.join(output_dir, f'{case_id}.txt')
    # Open a text file to save the results
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content.text)
    print(f"Content successfully saved to {filename}")
    

# fetch all case links from a directory page
def fetch_links(base_url):
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', class_='h5 gd-heardertext', href=True)
        # Filter out the URLs that are relevant
        case_links = [urljoin(base_url, link['href']) for link in links]
        return case_links
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []



url = "https://www.elitigation.sg/gd/s/2018_SGCA_56"
link_to_text(url, url.split('/')[-1], "dataset")





