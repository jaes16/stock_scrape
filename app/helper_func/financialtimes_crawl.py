import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept': 'text/html', 'Referer': 'http://www.google.com/'}

FT_BASE_ADDR = 'https://www.ft.com/'
FT_SECTIONS = {'Global Econ': 'global-economy', 'US Econ': 'us-economy',
                'Companies': 'companies', 'Technology': 'technology',
                'Markets': 'markets'}

def financialtimes_crawl():
    ret = {sect:[] for sect in FT_SECTIONS}

    for sect in FT_SECTIONS:
        req = requests.get(FT_BASE_ADDR+FT_SECTIONS[sect], headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        for article in soup.find_all('div', {'class':re.compile('o-teaser__content')}):
            try:
                #date = article.find('time')['datetime']

                tag = ""
                try:
                    tag = article.find('a', {'class' : re.compile('teaser__tag')}).text
                except:
                    pass
                title = article.find('a', {'class' : re.compile('teaser-heading')}).text
                link = article.find('a', {'class': re.compile('teaser-heading')})['href']
                descrip = article.find('a', {'class': re.compile('standfirst')}).text
                ret[sect].append({'title': title, 'tag': tag, 'description': descrip, 'link':link})
            except:
                pass
        time.sleep(2)
    
    return ret


def ft_article_crawl(url):
    print(url)
    req = requests.get('https://www.ft.com'+url, headers = headers)

    soup = BeautifulSoup(req.text, 'html.parser')

    article = json.loads(soup.find('script', {'type':'application/ld+json'}).text)['articleBody']

    return article.split('\n\n')


