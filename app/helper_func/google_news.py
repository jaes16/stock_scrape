import requests
import urllib.request
import time
import feedparser
import re
from datetime import datetime, timedelta
import math
import json
from time import sleep
from bs4 import BeautifulSoup

default_list = "amd, apple, ark innovation, nio, palantir, ..."

def func(search_term, fout):
    fout.write("<LI><h4>"+search_term+":\n")

    # get data from pushshift
    url = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&as_qdr=24&q="+search_term
    req = requests.get(url, headers = heads)

    # write to file
    f = open("google_news.xml", mode="wb")
    f.write(req.content)
    f.close

    # then read from said file
    y = feedparser.parse(r'google_news.xml')

    # start writing the titles to the html file
    fout.write("<UL>")
    for i in y.entries:
        fout.write("<LI><small><a href = \""+i.link+"\" target=\"_blank\">"+i.title+":</a></small></LI>\n")

    fout.write("</UL></h4>\n")


def google_news():
    output = open("Compiled News.html", mode="a")
    output.write("\n<h3>Google News:\n")

    # call function multiple times
    output.write("<UL>\n");
    term = input("\nGoogle News:\nEnter search term (type quit to quit):")
    while term != "quit":
        if term == "list":
            print(default_list)
        else :
            func(term, output)
            print("Sleeping so we don't get bounced...")
            sleep(4)
        term = input("Enter search term (type quit to quit):")

    output.write("</UL><h3>\n")
    output.close

def google_search(term, num):
	sleep(1)
	url = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&as_qdr=24&q="+term
	req = requests.get(url).text
	urls_titles = []
	y = feedparser.parse(req)
	for i in range(min(num, len(y.entries))):
		urls_titles.append([y.entries[i].link, y.entries[i].title])

	return urls_titles

def google_analyses_pdf(company, num):
	sleep(1)
	url = "https://www.google.com/search?q="+company+"+stock+analysis+filetype%3Apdf"
	req = requests.get(url).text
	url_pdfs = []
	soup = BeautifulSoup(req, "html.parser")
	tags = soup.body.find_all("div", class_="kCrYT")
	for tag in tags:
		if tag.a is not None and tag.div is not None and tag.div.div is None:
			if tag.find("div", class_=['BNeawe vvjwJb AP7Wnd']) is not None:
				origin = tag.find("div", class_="BNeawe UPmit AP7Wnd").text
				url_pdfs.append(["google.com"+tag.a['href'], tag.div.text[6:], origin[:origin.index(' ')]])

	return url_pdfs
