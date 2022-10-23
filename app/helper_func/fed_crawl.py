import requests
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


head = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
           'Accept': 'text/html', 'Referer': 'http://www.google.com/'}

base_url = "https://www.federalreserve.gov"
calendar_page = "/monetarypolicy/fomccalendars.htm"
statement_base_url = "/newsevents/pressreleases/monetary"
minutes_base_url = "/monetarypolicy/fomcminutes"
month_class = "fomc-meeting__month col-xs-5 col-sm-3 col-md-2"
day_class = "fomc-meeting__date col-xs-4 col-sm-9 col-md-10 col-lg-1"
statement_class = "col-xs-12 col-sm-8 col-md-8"

def fed_crawl_get_urls(years):
	time.sleep(1)
	base_page_source = requests.get(base_url+calendar_page, headers=head).text
	base_soup = BeautifulSoup(base_page_source, "html.parser")

	ret_arr = []
	dates = []
	for year in years:
		# statements
		tags = base_soup.find_all(href=re.compile(statement_base_url+year))
		for tag in tags:
			if tag.contents[0] == 'HTML':
				if tag.get('href').endswith('a.htm'):
					date = tag.get('href')[len(statement_base_url):-5]
					ret_arr.append([1,date])

		# minutes
		tags = base_soup.find_all(href=re.compile(minutes_base_url+year))
		for tag in tags:
			if tag.contents[0] == 'HTML':
				date = tag.get('href')[len(minutes_base_url):-4]
				ret_arr.append([2,date])
		'''
		if year == '2021':
			tag = base_soup.find("div", class_="panel panel-default")
			months = tag.find_all("div", class_=month_class)
			days = tag.find_all("div", class_=day_class)
			for i in range(len(months)):
				index = days[i].text.find('-')
				if days[i].text[index+2].isnumeric():
					dates.append(months[i].text+" "+days[i].text[index+1:index+3]+" 2021")
				else:
					dates.append(months[i].text+" "+days[i].text[index+1]+" 2021")
		'''

	return [ret_arr, dates]

def fed_crawl_get_statement(date):
	arr = []
	time.sleep(1)
	base_page_source = requests.get(base_url+statement_base_url+date+"a.htm").text
	base_soup = BeautifulSoup(base_page_source, "html.parser")
	article = base_soup.find("div", class_=statement_class)
	for p in article.find_all(name='p'):
		if p.a is None:
			arr.append(p.contents[0])

	return arr

def fed_crawl_get_minutes(date):
	arr = []
	time.sleep(1)
	base_page_source = requests.get(base_url+minutes_base_url+date+".htm").text
	base_soup = BeautifulSoup(base_page_source, "html.parser")
	article = base_soup.find("h3").find_next_siblings("p")
	title_count = 0
	for p in article:
		if p.find("strong") and not p.contents[0].find("strong"):
			if title_count >= 0:
				if p.contents[0].text == 'Voting for this action:':
					return arr
				arr.append([[p.contents[0].text]])
				if len(p.contents) > 2:
					arr[-1].append([p.contents[2]])
			title_count += 1
		elif title_count >= 1:
			if len(arr[-1]) > 1:
				arr[-1][1].append(p.getText())
			else:
				arr[-1].append([p.getText()])

	return arr


def fed_crawl_get_next_date():
	utc_time = datetime.utcnow()-timedelta(hours=5)
	