import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import pickle

page_size = 100
base_url = 'https://www.airlinequality.com'


def find_review(airline_name, rel_airline, total_page):
    ## --- find the content
    
    if total_page == 0:
        total_page = total_page+1
    else:
        total_page = total_page

    rel_airline = rel_airline
    list_df = []
    # df_main = pd.DataFrame()

    for i in range(1, total_page+1):
        url = f"{base_url}{rel_airline}/page/{i}/?sortby=post_date%3ADesc&pagesize={page_size}"
        
        r = requests.get(url)
        content = r.content
        parsed_content = bs(content, 'lxml')
        
        articles = parsed_content.find_all('article', attrs={'itemprop': 'review'})
        for article in articles:
            data = {}
            review_rating = {}
            
            # airline name
            airline = airline_name
            
            try: # id
                _id = article.find("div", attrs={"class": "body"})['id']
            except Exception as e:
                _id = ''
            
            try: # review
                review = article.find("div", attrs={"class": "text_content"}).get_text(' ', strip=True)
            except Exception as e:
                review = ''
            
            try: # rating
                rating = article.find("div", attrs={"itemprop": "reviewRating"}).get_text('', strip=True)
            except Exception as e:
                rating = ''
            
            try: # header
                header = article.find("div", attrs={"class": "body"}).find('h2', attrs={"class": "text_header"}).get_text('', strip=True)
            except Exception as e:
                header = ''
            
            try: # sub-header
                sub_header = article.find("div", attrs={"class": "body"}).find('h3', attrs={"class": "text_sub_header"}).get_text(' ', strip=True)
            except Exception as e:
                sub_header = ''
            
            try: # author
                author = article.find("div", attrs={"class": "body"}).find('h3', attrs={"class": "text_sub_header"}).find('span', attrs={"itemprop": "author"}).get_text('', strip=True)
            except Exception as e:
                author =  ''
            
            try: # time_published
                time_published = article.find("div", attrs={"class": "body"}).find('h3', attrs={"class": "text_sub_header"}).find('time', attrs={"itemprop": "datePublished"}).get_text('', strip=True)
            except Exception as e:
                time_published =  ''      
        
        
            data = {
                'airline':airline,
                'id': _id,
                'review':review,
                'rating' :rating, 
                'header' :header,
                'sub_header' :sub_header,
                'author' :author,
                'time_published' :time_published
            }
            
            # review_ratings
            rows = article.find('table', attrs={'class': 'review-ratings'}).find_all('tr')
            for row in rows:
                td = row.find_all('td')
                try:
                    head = td[0].get_text(strip=True)   
                except Exception as e: 
                    head = ''
                    
                try:
                    vals = td[-1].select('span.star.fill')
                    val = vals[-1].get_text(strip=True)
                except Exception as e:
                    try:
                        val = td[-1].get_text(strip=True)     
                    except Exception as e:
                        val = ''
                    
                review_rating[head] = val
        
            data.update(review_rating)
            list_df.append(data)
        
        print(f'Sleep! (1 sec), scrapped {i} pages')
        time.sleep(1)
        

        ## --- dict to dataframe & concat to main df per page
        # df_main = pd.concat([df_main, df], axis=0, join='outer', ignore_index=True)
        
    # save to csv per airline
    df = pd.DataFrame.from_dict(list_df)
    df.to_csv(f'.\\dataset\\df_review_{airline_name}.csv', index=False, sep=';')

    return None



## --- read rel-link & total page airlines
air_urls_pages = pickle.load(open('list_air_url_page.pkl', 'rb'))
length = len(air_urls_pages)


for index, item in enumerate(air_urls_pages):
    rel_airline = item[0]
    total_page = int(item[1])
    airline_name = item[2]
    
    print(f'{airline_name} on progress!')
    find_review(airline_name, rel_airline, total_page)
    
    ## --- indicator
    print(f'{airline_name} scrapped! index = ({index} of {length} length)')
    
