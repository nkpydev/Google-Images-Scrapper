import os,re,json,sys,time
from json import JSONDecodeError
import requests
from requests.exceptions import SSLError
from os.path import exists
from bs4 import BeautifulSoup

def save_image(img_link,img_name,img_type):
        try:
            img = requests.get(img_link,stream=True)
            with open(os.path.join(KEYWORD_DIR,img_name + '.' + img_type), 'wb') as f:
                for chunk in img.iter_content(1024):
                    f.write(chunk)    
        except SSLError:
            print('SSL Error, Image from this link cannot be downloaded!!')

image_types = ["jpeg", "jpg", "png", "gif", "tiff", "psd", "raw"]

if __name__ == "__main__":
    query = input("\nEnter your query:\t")
    print("========PROCESSING==========")
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    IMG_BASE_DIR = os.path.join(BASE_DIR,'Images')
    KEYWORD_DIR = os.path.join(IMG_BASE_DIR,query)
    if not exists(KEYWORD_DIR):
        os.makedirs(KEYWORD_DIR)
    dict_store = []
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    headers = { 'User-Agent': USER_AGENT }
    google_img_query = "https://www.google.com/search?q=" + query + "&source=lnms&tbm=isch"

    r = requests.get(google_img_query,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    response_div = soup.find_all('div',attrs={'class': 'rg_meta notranslate'})

    for entry in response_div:
        str_entry = str(entry)
        pattern = r'\"\>([a-zA-Z0-9\_\:\{\"\-\,\.\/\/\|\?\\\} ])+'
        match = re.search(pattern,str_entry)
        if match:
            tmp1 = match.group()
            tmp2 = tmp1.replace(">", '')
            tmp3 = tmp2.replace('"{', '\n{')
            x = tmp3.split('\n')
            for new_entry in x:
                try:
                    tt = json.loads(new_entry)
                    dict_store.append(tt)
                except JSONDecodeError:
                    pass
    img_counter = 0   
    for dict_entry in dict_store:
        if dict_entry['ou']:
            img_counter += 1
    print("\nTotal images to download are:\t{}".format(img_counter))
    
    for dict_entry in dict_store:
        if len(dict_store) != 0:
            try:
                if dict_entry['ou'] and (':' not in dict_entry['id']) and dict_entry['ity'] != '':
                    save_image(dict_entry['ou'],dict_entry['id'],dict_entry['ity'])
                elif dict_entry['ou'] and dict_entry['ity'] != '':
                    if ':' in dict_entry['id']:
                        updated_id = dict_entry['id'].replace(':','')
                        save_image(dict_entry['ou'],updated_id,dict_entry['ity'])
                else:
                    if dict_entry['ou'] and (':' not in dict_entry['id']) and dict_entry['ity'] == '':
                        for imge_type in image_types:
                            if imge_type in dict_entry['ity']:
                                save_image(dict_entry['ou'],dict_entry['id'],imge_type)
                # sys.stdout.write('[%-100s] %d%%' %('█'*dict_store.index(dict_entry) + ''+ dict_store.index(dict_entry)))
                # sys.stdout.flush()
                # time.sleep(0.25)
            except KeyboardInterrupt:
                print("\nYou stopped the process!!")
                exit()
        else:
            pass