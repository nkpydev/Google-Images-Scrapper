import os,re
import requests
from requests.exceptions import SSLError
from os.path import exists

def get_image_name_and_type(link):
        temp_split = link.split('/')
        img_info = temp_split[-1].split('.')
        return img_info[-2],img_info[-1]

def save_image(link):
    img_name,img_type = get_image_name_and_type(link)
    try:
        img = requests.get(link,stream=True)
        with open(os.path.join(KEYWORD_DIR,img_name + '.' + img_type), 'wb') as f:
            for chunk in img.iter_content(1024):
                f.write(chunk)    
    except SSLError:
        print('SSL Error, Image from this link cannot be downloaded!!')

    
if __name__ == '__main__':
    BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    user_input = input('\nEnter your Query here:\t')
    IMG_BASE_DIR = os.path.join(BASE_DIR,'Images')
    KEYWORD_DIR = os.path.join(IMG_BASE_DIR,user_input)
    if not exists(KEYWORD_DIR):
        os.makedirs(KEYWORD_DIR)
    USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    headers = { 'User-Agent': USER_AGENT }
    gogl_img_query = "https://www.google.com/search?q=" + user_input + "&rlz=1C1GCEU_enIN821IN821&source=lnms&tbm=isch&sa=X&ved=0ahUKEwj07uOZgP3hAhUM6Y8KHRqhCJwQ_AUIESgE&biw=1920&bih=969"
    r = requests.get(gogl_img_query,headers=headers)
    img_link_collection = [n for n in re.findall('"ou":"([a-zA-Z0-9_./:-]+.(?:jpg|jpeg|png|gif))",', r.text)]
    try:
        print('Started saving images!!')
        for link in img_link_collection:
            save_image(link)
    except KeyboardInterrupt:
        print('Stopped!!')