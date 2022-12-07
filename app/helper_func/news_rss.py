import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import time
import json

from app.helper_func.financialtimes_crawl import financialtimes_crawl
from app.helper_func.bloomberg_crawl import bloomberg_crawl

from app.helper_func.word_tagging import get_keywords

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept': 'text/html', 'Referer': 'http://www.google.com/'}

NYT_ADDR = "https://rss.nytimes.com/services/xml/rss/nyt/"
NYT_SECTIONS = ['Business', 'Economy', 'Technology']

WP_ADDR = "https://feeds.washingtonpost.com/rss/" + "?itid=lk_inline_manual_42"
WP_SECTIONS = {'Politics':'politics', 'Tech':'business/technology', 'Business':'business'}

CNBC_ADDR = "https://www.cnbc.com/id//device/rss/rss.html"
CNBC_SECTIONS = {'Business':'10001147', 'Earnings':'15839135', 'Commentary':'100370673', 'Economy':'20910258',
                'Finance':'10000664', 'Technology':'19854910', 'Politics':'10000113'}

WSJ_ADDR = "https://feeds.a.dj.com/rss/"
WSJ_SECTIONS = {'US Business': 'WSJcomUSBusiness', 'Market':'RSSMarketsMain', 'Tech': 'RSSWSJD'}

DATE_LIMIT = datetime.today().date() - timedelta(days=1)

def nyt_crawl():
    ret = {sect:[] for sect in NYT_SECTIONS}

    for sect in NYT_SECTIONS:
        req = requests.get(NYT_ADDR + sect + '.xml', headers = headers)
        # catch request error here and/or catch exceptions
        # catch Exception as e:
        # if req.status_code != 200:

        soup = BeautifulSoup(req.text, 'lxml')

        articles = soup.findAll('item')

        for article in articles:
            try:
                date = article.find('pubdate').text[:-6]

                # check date
                if datetime.strptime(date[5:], '%d %b %Y %H:%M:%S').date() < DATE_LIMIT:
                    continue
                
                # add to section
                title = article.find('title').text
                description = article.find('description').text
                tags = [cat.text for cat in article.findAll('category')]
                link = article.find('atom:link')['href']

                ret[sect].append({'title': title, 'desc': description, 'tags': tags, 'link': link, 'date': date})
            except:
                pass
        
        time.sleep(1)
            
    return ret

        
def cnbc_crawl():
    ret = {sect:[] for sect in CNBC_SECTIONS}

    for sect in CNBC_SECTIONS:

        req = requests.get(CNBC_ADDR[:24] + CNBC_SECTIONS[sect] + CNBC_ADDR[24:], headers = headers)
        # catch request error here and/or catch exceptions
        # catch Exception as e:
        # if req.status_code != 200:

        soup = BeautifulSoup(req.text, 'html.parser')

        articles = soup.find_all('item')

        for article in articles:
            try:
                date = article.find('pubdate').text[:22]

                # check date
                if datetime.strptime(date[5:], '%d %b %Y %H:%M').date() < DATE_LIMIT:
                    continue
                
                # add to section
                title = article.find('title').text
                description = article.find('description').text
                link = list(article.children)[2].strip()

                ret[sect].append({'title': title, 'desc': description, 'link': link, 'date': date})
            except:
                pass

        time.sleep(1)

    return ret


def wp_crawl():
    ret = {sect:[] for sect in WP_SECTIONS}

    for sect in WP_SECTIONS:

        req = requests.get(WP_ADDR[:37] + WP_SECTIONS[sect] + WP_ADDR[37:], headers = headers)
        # catch request error here and/or catch exceptions
        # catch Exception as e:
        # if req.status_code != 200:

        soup = BeautifulSoup(req.text, 'html.parser')

        articles = soup.find_all('item')

        for article in articles:
            try:
                date = article.pubdate.text[:-4]

                # check date
                if datetime.strptime(date[5:], '%d %b %Y %H:%M:%S').date() < DATE_LIMIT:
                    continue
                
                # add to section
                title = article.title.text
                description = article.description.text
                link = article.guid.text

                ret[sect].append({'title': title, 'desc': description, 'link': link, 'date': date})
            except:
                pass

        time.sleep(1)

    return ret


def wsj_crawl():
    ret = {sect:[] for sect in WSJ_SECTIONS}

    for sect in WSJ_SECTIONS:

        req = requests.get(WSJ_ADDR + WSJ_SECTIONS[sect] + '.xml', headers = headers)
        # catch request error here and/or catch exceptions
        # catch Exception as e:
        # if req.status_code != 200:

        soup = BeautifulSoup(req.text, 'html.parser')

        articles = soup.find_all('item')

        for article in articles:
            try:
                date = article.pubdate.text[:-6]

                # check date
                if datetime.strptime(date[5:], '%d %b %Y %H:%M:%S').date() < DATE_LIMIT:
                    continue
                
                # add to section
                title = article.title.text
                description = article.description.text
                link = list(article.children)[4]

                ret[sect].append({'title': title, 'desc': description, 'link': link, 'date': date})
            except:
                pass
        time.sleep(1)

    return ret


def helper_assorted_news():

    data = {'date': datetime.today().strftime("%Y-%b-%d")}
    word_cloud = {}

    try:
        bloom = bloomberg_crawl()
        data['Bloomberg'] = bloom
        word_cloud = get_keywords(bloom, word_cloud)                
    except:
        pass
    try:
        nyt = nyt_crawl()
        data['NYT'] = nyt
        word_cloud = get_keywords(nyt, word_cloud)
    except:
        pass
    try:
        wp = wp_crawl()
        data['WP'] = wp
        word_cloud = get_keywords(wp, word_cloud) 
    except:
        pass
    try:
        cnbc = cnbc_crawl()
        data['CNBC'] = cnbc
        word_cloud = get_keywords(cnbc, word_cloud) 
    except:
        pass
    try:
        wsj = wsj_crawl()
        data['WSJ'] = wsj
        word_cloud = get_keywords(wsj, word_cloud) 
    except:
        pass
    try:
        ft = financialtimes_crawl()
        data['FT'] = ft
        word_cloud = get_keywords(ft, word_cloud) 
    except:
        pass
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open('wordcloud.json', 'w', encoding='utf-8') as f:
        json.dump(word_cloud, f, ensure_ascii=False, indent=4)
