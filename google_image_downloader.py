# GoogleImages - Image Scrapper 
# Version: 1.1.0

# --- Lib Imports --- #
import re
import os
import json
import time
import requests
from tqdm import tqdm
from os.path import exists
from bs4 import BeautifulSoup
from selenium import webdriver
from requests.exceptions import SSLError 
from selenium.webdriver import Chrome, ChromeOptions

global headers

# --- Headers to set User-Agent --- #
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

# --- Function to Download/Save the Image Locally --- #
def save_image(user_search_term, dict_entry):
    # --- Base Image Directory --- #    
    IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),'GIS_Images')    
    if not exists(IMG_DIR):
        os.makedirs(IMG_DIR)
    # --- Search Term Directory inside Base Image Directory --- #
    SEARCH_TERM_DIR = os.path.join(IMG_DIR, user_search_term)
    if not exists(SEARCH_TERM_DIR):
        os.makedirs(SEARCH_TERM_DIR)
    # --- Actual Request with Stream=True --- #
    try:
        dwn_res = requests.get(str(dict_entry['img_link']), stream=True)
        # --- Saving the file with SearchTerm + Counter + Type --- #
        file_path = os.path.join(SEARCH_TERM_DIR, (user_search_term + '_' + str(dict_entry['ID']) + '.' + dict_entry['img_type']))                    
        with open(file_path, 'wb') as f:
            for chunk in dwn_res.iter_content(1024):
                f.write(chunk)
    except SSLError:
        pass
    except TimeoutError:
        pass
    except ConnectionError:
        pass
    except Exception:
        pass

# --- Take Search Term input from End-User --- #
user_search_term = input("\nEnter your Search Term:\t")
# --- Convert user search term into Query to check Google Images --- #
query = f'https://www.google.com/search?tbm=isch&q={user_search_term}'
c_options = ChromeOptions()
# --- Intialize a Chrome Driver --- #
browser = Chrome(executable_path='chromedriver.exe',chrome_options=c_options)
# --- Naviagate to the Google Images Link with Query --- #
browser.get(query)
# --- Sleep --- #
time.sleep(2)
#--- Scroll till all Results are available ---#
scroll_pause_time = 1
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
# --- End of JS --- #

# --- HTML Content --- #
html_content = browser.page_source
# --- List to store all Dicts --- #
img_info_list = []
# --- Parse that original content with Beautiful Soup --- #
soup = BeautifulSoup(html_content, 'html.parser')
# --- Check for all DIVs that contain Img-Info Dict --- #
img_div = soup.find_all('div', attrs={'class': 'rg_meta notranslate'})
# --- Iterate thr' each DIV entry in "img_div" --- #
# --- Parse it to clear html tags and Load Dict like data into JSON --- #
for entry in img_div:
    if entry:            
        entry = str(entry).replace('<div class="rg_meta notranslate">','')
        entry = entry.replace('</div>','')
        _tmp = json.loads(entry)
        img_info_list.append(_tmp)
# --- Downloadable dict(ImgInfo)/s into a List --- #
download_tracker_list = []
# --- Counter for ID --- #
counter_img = 1
# --- Iterate thr' "img_info_list", to count all Downloadable Images --- #
for img_entry in img_info_list:
    if img_entry['ity']:
        download_tracker_list.append({'ID': counter_img,'img_link': img_entry['ou'], 'img_type': img_entry['ity']})        
        counter_img += 1
browser.quit()
# --- Print Total Downloadable Images --- #
print(f"Total Downloadable Images are:\t{len(download_tracker_list)}")

# --- Progress Bar with TQDM Lib --- #
with tqdm(total=len(download_tracker_list)) as pbar:
    for dict_entry in download_tracker_list:
        try:
            save_image(user_search_term, dict_entry)            
            pbar.update(1)
        except KeyboardInterrupt:
            print("\nYou killed the Process!!")
            exit()