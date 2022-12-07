import requests
import re
import time
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver.v2 as uc
import json

useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/605.1.15"

DATE_LIMIT = datetime.today().date() - timedelta(days=1)

BLOOMBERG_SECTIONS = {'Markets': 'markets', 'Industries': 'industries', 'Technology': 'technology',} #'Economics': 'economics', 'Politics': 'politics',
                    #{'Wealth': 'wealth', 'Opinion': 'opinion',}]# 'Businessweek': 'businessweek'}]


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept': 'text/html', 'Referer': 'http://www.google.com/'}





'''
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-infobars')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(executable_path= './chromedriver', options = options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
'''

base_url = "https://www.bloomberg.com"

def bloomberg_article_crawl(url):

    options = Options()
    options.headless = True

    driver = uc.Chrome(options)
    if "https://" in url:
        driver.get(url)
    else:
        driver.get('https://www.bloomberg.com'+url)
    #frame = driver.find_eledment(By.XPATH, '//iframe[@id="reg-ui-client__iframe"]')

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    js = json.loads(soup.find('script', {'data-component-props':'OverlayAd'}).text)
    soup2 = BeautifulSoup(js['story']['body'], 'html.parser')

    driver.quit()

    return [p.text for p in soup2.find_all('p')]


def bloomberg_page_crawl(driver):
    titles = []

    '''
    soup = BeautifulSoup(source, 'html.parser')

    for article in soup.find_all('a', {'href': re.compile('news/articles/')}):
        try:
            link = article['href']
            title = article.text.strip()
            if article.find('img'):
                title = article.find('img')['alt']
            pubdate = article['href']
            pubdate_ind = pubdate.index('articles/'+datetime.today().strftime('%Y')) + 9
            pubdate = pubdate[pubdate_ind : pubdate_ind + 10]
            if datetime.strptime(pubdate, '%Y-%m-%d').date() < DATE_LIMIT:
                continue
            if title not in titles:
                titles[title] = {'date': pubdate, 'link': link}
        except:
            pass
    '''
    for article in driver.find_elements(By.XPATH, '//article'):
        try:
            link = article.find_element(By.XPATH, ".//a[contains(@class,'headline')]")
            title = link.text.strip()
            if title == "":
                continue
            for art in titles:
                if art['title'] == title:
                    # don't include this duplicate article
                    1/0
            pubdate = link.get_attribute('href')
            pubdate_ind = pubdate.index('articles/'+datetime.today().strftime('%Y')) + 9
            pubdate = pubdate[pubdate_ind : pubdate_ind + 10]
            if datetime.strptime(pubdate, '%Y-%m-%d').date() < DATE_LIMIT:
                continue
            titles.append({'title': title, 'date': pubdate, 'link': link.get_attribute('href')})
        except Exception as e:
            pass

    return titles



def bloomberg_crawl():
    ret = {}

    
    #for sect_arr in range(2):
    #options = webdriver.ChromeOptions()
    #options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    #driver = uc.Chrome(options)
    #driver = uc.Chrome()

    '''
        try:
            frame = WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//iframe[@title="SP Consent Message"]')) 
            #frame = driver.find_element(By.XPATH, '//iframe[@title="SP Consent Message"]')
            driver.switch_to.frame(frame)
            driver.find_element(By.XPATH, '//button[@title="Yes, I Accept"]').click()
            driver.switch_to.default_content()
        except:
            pass
        
        element_navi = WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//a[@class="navi-edition__button"]'))
        element_navi.click()
        element_amer = WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//a[@data-edition-code="amer"]'))
        element_amer.click()
        source = driver.page_source
    '''
    driver = uc.Chrome()
    driver.get('https://www.bloomberg.com/')

    #for sect in BLOOMBERG_SECTIONS[sect_arr]:
    for sect in BLOOMBERG_SECTIONS:
        try:
            #options = Options()
            #options.headless = True

            # driver.get('https://www.bloomberg.com/'+BLOOMBERG_SECTIONS[sect])
            # print('https://www.bloomberg.com/'+BLOOMBERG_SECTIONS[sect])
            driver.execute_script("window.scrollTo(0, 0);")
            element_navi = WebDriverWait(driver, 15).until(lambda x: x.find_element(By.XPATH, '//li[@data-section="'+sect+'"]/a'))
            element_navi.click()

            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ret[sect] = bloomberg_page_crawl(driver) 
            # driver.quit()
        except Exception as e:
            print(e, sect, "\n")               
    
    driver.get('https://www.google.com/')
    driver.quit()
    return ret

# print(bloomberg_crawl())

