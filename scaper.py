import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def url_to_file(url,case_id,output_dir):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('div', id='divJudgement')
        
        # Extract and print the text
        # Extract and save the text if content is found
        if content:
            text = content.get_text()
            
            # Define the file path
            filename = os.path.join(output_dir, f'{case_id}.txt')
            # Write the text to a file
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"Content successfully saved to {filename}")
        else:
            print("Content not found")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")      
#url = "https://www.elitigation.sg/gd/s/2015_SGHC_289"
#url_to_file(url, "1.txt")

def fetch_links(base_url):
    # Function to fetch all case links from a directory page
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


def links_to_files(links, output_dir):
    for i in range(len(links)):
        url_to_file(links[i],f"{links[i].split('/')[5]}",output_dir)
    print("scraping completed")
        
url="https://www.elitigation.sg/gd/Home/Index?filter=SUPCT&yearOfDecision=All&sortBy=Score&currentPage=1&sortAscending=False&searchPhrase=tort&verbose=False"
links=fetch_links(url)
links_to_files(links, 'tort cases')






