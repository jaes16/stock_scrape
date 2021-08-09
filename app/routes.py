from datetime import datetime
from pytz import timezone
from flask import render_template, flash, redirect, url_for, request
from app import current_app
from app.forms import GoogleSearchForm, RedditSubForm, TwitterSearchForm
from app.helper_func.fed_crawl import fed_crawl_get_urls, fed_crawl_get_statement, fed_crawl_get_minutes
from app.helper_func.google_news import google_search, google_analyses_pdf
from app.helper_func.reddit_pushshift import get_reddit_feed
from app.helper_func.twitter_api import get_tweets

@current_app.route('/')
@current_app.route('/home')
def home():
    return render_template('main/home.html', title='Home')



@current_app.route('/loading/<go_url>')
def loading(go_url):
	data = go_url.split('-')
	url = data[0]
	args = data[1:]
	return render_template('main/loading.html', title='Loading...', url=url, args=args)



@current_app.route('/fomc')
def fomc():
	ret = fed_crawl_get_urls(['2021'])
	urls = ret[0]
	'''
	tz = timezone('EST')
	next_date = datetime.now(tz).date()
	for date in ret[1]:
		if datetime.strptime(date, '%B %d %Y').date() >= next_date:
			next_date = datetime.strptime(date, '%B %d %Y').date()
			break
	'''
	return render_template('main/fomc.html', title='FOMC', urls=urls) #, next_date=next_date.strftime("%d %B, %Y"))

@current_app.route('/fomc_statement/<args>')
def fomc_statement(args):
	# to do: have to make sure we don't crash when users put in custom dates
	lines = fed_crawl_get_statement(args)
	return render_template('main/fomc_statements.html', title='FOMC Statement', date=args, lines=lines[1:-1])

@current_app.route('/fomc_minutes/<args>')
def fomc_minutes(args):
	# to do: have to make sure we don't crash when users put in custom dates
	sections = fed_crawl_get_minutes(args)
	return render_template('main/fomc_minutes.html', title='FOMC Minutes', date=args, sections=sections, len_sec=len(sections))



@current_app.route('/reddit', methods=['GET', 'POST'])
def reddit():
	form = RedditSubForm()
	if form.validate_on_submit():
		url_title_text = []
		time = form.days.data
		subs = [form.subr1.data, form.subr2.data, form.subr3.data, form.subr4.data, form.subr5.data]
		num_subs = 0
		#debug_message=''
		for sub in subs:
			if sub:
				num_subs += 1
				url_title_text.append(get_reddit_feed(sub, time))
		#return render_template('main/reddit.html', debug_message=debug_message)
		return render_template('main/reddit.html', title='Reddit Posts', subs=subs, titles=url_title_text, form=form, num_subs=num_subs)
	else:
		return render_template('main/reddit.html', title='Reddit Posts', form=form, num_subs=0)


@current_app.route('/google_news', methods=['GET', 'POST'])
def google_news():
	form = GoogleSearchForm()
	if form.validate_on_submit():
		titles = []
		terms = [form.term1.data, form.term2.data, form.term3.data, form.term4.data, form.term5.data]
		num_terms = 0
		for term in terms:
			if term:
				num_terms += 1
				titles.append(google_search(term.replace(' ', '+'), 10))

		return render_template('main/google_news.html', title='Google News', terms=terms, titles=titles, form=form, num_terms=num_terms)
	else:
		return render_template('main/google_news.html', title='Google News', form=form, num_terms=0)




@current_app.route('/google_analyses', methods=['GET', 'POST'])
def google_analyses():
	form = GoogleSearchForm()
	if form.validate_on_submit():
		url_pdfs = []
		terms = [form.term1.data, form.term2.data, form.term3.data, form.term4.data, form.term5.data]
		num_terms = 0
		for term in terms:
			if term:
				num_terms += 1
				url_pdfs.append(google_analyses_pdf(term.replace(' ', '+'), 10))

		return render_template('main/google_analyses.html', title='Google Analyses', terms=terms, url_pdfs=url_pdfs, form=form, num_terms=num_terms)
	return render_template('main/google_analyses.html', title='Google Analyses', form=form, num_terms=0)



@current_app.route('/assorted_news')
def assorted_news():
	return render_template('main/assorted_news.html', title='Assorted News')

@current_app.route('/twitter', methods=['GET', 'POST'])
def twitter():
	form = TwitterSearchForm()
	if form.validate_on_submit():
		feeds = []
		users = []
		form_data = [form.user1.data, form.user2.data, form.user3.data, form.user4.data, form.user5.data]
		for user in form_data:
			if user:
				users.append(user)
				try:
					feeds.append(get_tweets(user))
				except Exception as ex:
					feeds.append([[" ", "No such user."]])

		return render_template('main/twitter.html', title='Twitter Feeds', feeds=feeds, users=users, form=form, num_users=len(users))
	return render_template('main/twitter.html', title='Twitter Feeds', form=form)
