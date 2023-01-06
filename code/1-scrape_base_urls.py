import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pickle


base_urls = {}
url = 'https://www.airlinequality.com/review-pages/a-z-airline-reviews/'

r = requests.get(url)
content = r.content
parsed_content = bs(content, 'lxml')

tabs = parsed_content.find('div', attrs={'class': 'tabs-content'})
a2z = tabs.find_all('div', attrs={'class': 'content'})

for index, initial in enumerate(a2z):
    groups = initial.find_all('div', attrs={'class': 'a_z_col_group'})
    
    for group in groups:
        li_s = group.find_all('li')
        
        for li in li_s:
            name = li.find('a').get_text(' ', strip=True)
            link = li.find('a')['href']
            base_urls[name] = link
            
    print(f'initial {index} scrapped')
            

pickle.dump(base_urls, open('dict_base_urls.pkl', 'wb'))
           
df = pd.DataFrame.from_dict(base_urls, orient='index')
df.to_csv(f'df_base_urls.csv', index=True, sep=';')