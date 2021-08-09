import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import math
import json
from time import sleep

heads = {'User-Agent': 'Mozilla/5.0'}

score = "1"

default_list = "stocks, StockMarket, investments, WSB, etc..."

def func(subreddit, fout, days):
    # find days to read for
    now = datetime.utcnow()
    then = now - timedelta(int(days))
    now_str = str(math.trunc(now.timestamp()))
    then_str = str(math.trunc(then.timestamp()))

    # write out name of subreddit
    fout.write("<h4>"+subreddit+":\n")

    # get data from pushshift
    url = "http://api.pushshift.io/reddit/search/submission/?sort=desc&sort_type=created_utc&after="+then_str+"&before="+now_str
    url += "&score=>"+score+"&subreddit="+subreddit
    req = requests.get(url, headers = heads)

    # write to file, just in case it is needed again
    f = open("reddit_pushshift.json", mode="wb")
    f.write(req.content)
    f.close

    # then read from said file
    f = open("reddit_pushshift.json", mode="r")
    y = json.loads(f.read())

    # start writing the titles to the html file
    fout.write("<UL>")
    for i in y.get("data"):
        fout.write("<LI><a href = \""+i.get("url")+"\" target=\"_blank\">"+i.get("title")+":</a>\n")
        fout.write("<small><small>"+i.get("selftext")+"</small></small></LI>")

    f.close
    fout.write("</UL></h4>\n")


def reddit_pushshift():
    output = open("Compiled News.html", mode="a")
    output.write("\n<h3>Reddit:\n")

    # call function multiple times
    output.write("<UL>\n");
    subreddit = input("\nReddit:\nEnter subreddit to search (type quit to quit):")
    while subreddit != "quit":
        if subreddit == "list":
            print(default_list)
        else:
            days_in = input("Enter days:")
            func(subreddit, output, days_in)
            print("Sleeping so we don't get blocked...")
            sleep(1)

        subreddit = input("Enter subreddit to search (type quit to quit):")

    output.write("</UL></h3>\n")
    output.close


def get_reddit_feed(sub, time, size):
	sleep(1)

	url = "https://api.pushshift.io/reddit/search/submission/?size=10&after="+str(time)+"d&sort_type=score&selftext:not=removed&subreddit="+sub

	req = requests.get(url, headers = heads)
	y = json.loads(req.text)

	ret_arr = []

	for i in y.get("data"):
		ret_arr.append([i.get("url"), i.get("title"), i.get("selftext")])

	return ret_arr

def get_sub_comments(sub, term, time, size):
	sleep(1)

	url = "https://api.pushshift.io/reddit/search/submission/?q={}&after={}d&sort_type=score&selftext:not=removed&subreddit={}&size={}".format(term, str(time), sub, str(size))

	req = requests.get(url, headers = heads)
	y = json.loads(req.text)

	ret_arr = []

	for i in y.get("data"):
		ret_arr.append(i)

	return ret_arr

def get_all_comments(sub, term, size):
	sleep(1)

	url = "https://api.pushshift.io/reddit/search/submission/?q={}&sort_type=score&selftext:not=removed&subreddit={}&size={}".format(term, sub, str(size))

	req = requests.get(url, headers = heads)
	y = json.loads(req.text)

	ret_arr = []

	for i in y.get("data"):
		ret_arr.append(i)

	return ret_arr
