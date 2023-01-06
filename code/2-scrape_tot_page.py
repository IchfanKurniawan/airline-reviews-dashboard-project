import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pickle

page_size = 100
base_url = 'https://www.airlinequality.com'
urls_pages = {}

## --- read rel-link airlines
base_urls = pickle.load(open('dict_base_urls.pkl', 'rb'))


## --- find total pages & save
for index, (key, val) in enumerate(base_urls.items()):
    url = f"{base_url}{val}/?sortby=post_date%3ADesc&pagesize={page_size}"

    r = requests.get(url)
    content = r.content
    parsed_content = bs(content, 'lxml')

    try:
        article = parsed_content.find('article', attrs={'class': 'comp_reviews-pagination'})
        li_s = article.find_all('li')
        total_page = li_s[-2].get_text(' ', strip=True)
    except Exception as e:
        total_page = 0
        
    ## --- save
    urls_pages[key] = [val, total_page]

    ## --- progress
    if index%5 == 0: print(f'scrapped {index} records!')

## --- dump
pickle.dump(urls_pages, open('dict_urls_pages.pkl', 'wb'))