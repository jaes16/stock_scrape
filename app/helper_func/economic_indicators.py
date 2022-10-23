import requests
import re
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
            'Accept': 'text/html', 'Referer': 'http://www.google.com/'}

US_GDP_ADDR = 'https://ycharts.com/indicators/us_monthly_gdp'
US_CPI_ADDR = 'https://www.bls.gov/feed/cpi.rss'
US_UNEMP_ADDR = 'https://data.bls.gov/timeseries/LNS14000000'

def get_us_gdp():
    req = requests.get(US_GDP_ADDR, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    ret = {}

    for panel in soup.find_all('div',{'class':'panel-data'}):
        title = panel.find('h3', {'class':'panel-title'})
        if title and title.text == 'Historical Data':
            for tr in panel.find('tbody').find_all('tr'):
                date_str = tr.find('td').text.strip()
                gdp = tr.find_all('td')[1].text.strip()
                date = datetime.strptime(date_str, "%B %d, %Y")
                if date.date() < (datetime.today().date() - timedelta(days=183)):
                    break
                ret[date_str] = gdp
            break

    return ret


def get_us_cpi():
    req = requests.get(US_CPI_ADDR, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    ret = {}

    for entry in soup.find_all('entry'):
        text = entry.find('content').text
        month_ind = text.index('Consumer Price Index for All Urban Consumers rose')+50
        monthly = text[month_ind:month_ind+3]
        cumul_ind = text.index(' percent over the last 12 months')
        cumulative = text[cumul_ind-3:cumul_ind]
        date = datetime.strptime(entry.find('published').text[:7], '%Y-%m')
        month = date.strftime('%B %Y')

        ret[month] = {'month': monthly, 'cumulative': cumulative}
    
    return soup,ret


def get_us_unemp():

    req = requests.get(US_CPI_ADDR, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    ret = {}

    table = soup.find('table', {'id':'table0'}).find('tbody')
    tr1 = table.find_all('tr')[-1].find_all('td')
    tr2 = table.find_all('tr')[-2].find_all('td')

    for i in range(len(tr1)):
    tr1[-(i+1)].text
    12-i