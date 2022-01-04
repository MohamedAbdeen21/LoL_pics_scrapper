# Import os, regular expression for parsing, time, requests, io and Image from Pillow
import os 
import re
import time 
import requests
from io import BytesIO
from PIL import Image


os.chdir(f'{os.path.dirname(os.path.realpath(__file__))}'+r'/all_champs')

def scrape_links(home_url = 'https://lol.fandom.com/wiki/Category:Champion_Skin_Loading_Screens'):
    # Initialize visited_urls list to save all the previously visited urls, and all_links list to save all image links. 
    visited_urls = []
    all_links = []

    # URL of the first page of the wiki
    
    url = home_url
    while True:
        # if the url was already visited, break
        if url in visited_urls:
            break
        else:
            # Else, get the html of the url, parse all image links and save them to all_links, parse for the link of previous and next page and run the loop
            # with the next page url
            response = requests.get(url)
            html_file = response.content.decode('utf-8')
            all_links = all_links + re.findall('<a href="(.+?)" class="image"',html_file)
            visited_urls.append(url)

            next_link = "https://lol.fandom.com/" + re.findall('<a href="(/wiki/Category:Champion_Skin_Loading_Screens.+?)" class="to_hasTooltip"',html_file)[-1]
            url = next_link
            print(all_links)

    return(all_links)


def download_and_save():
    # Get the list of all_links from scrape_links function
    links_list = scrape_links()

    # For debugging
    #initial = time.perf_counter()

    # For each link, get the name of the skin, if the name already exists in target folder, skip
    # else, append to the folder
    for link in links_list:
        name = re.findall('Screen_(.+?\.jpg)',link)[0]
        if os.path.isfile(name):
            print(f'{name} exists!')
            continue
        else:
            res = requests.get(link)
            img1 = BytesIO(res.content)
            time.sleep(1)
            img2 = Image.open(img1)
            img2.save(name)
            print(f'{name} created!')
            
    # For debugging
    #print(time.perf_counter()-initial)

if __name__ == "__main__":
    download_and_save()


