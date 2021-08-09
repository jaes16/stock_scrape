import requests
import os
import json
TWITTER_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAJ80SAEAAAAAmecN1QNQ8Mo%2BnfwyVmOLkznFTuY%3D5pfbcunbMoZcd05I8UtrqDXq3GfTr2uVPOGJgEK031g7dxxyuH'
TWITTER_KEY = '88Gigv2gzzH6SMW34BTkVmwo6'
TWITTER_SECRET_KEY = 'JES6pHZZiiaRwAka1jpSpOFa5Cwm8EP0eDY8exxsNrU6vmS8Zq'


def bearer_oauth(r):
	"""
	Method required by bearer token authentication.
	"""

	r.headers["Authorization"] = f"Bearer {TWITTER_BEARER_TOKEN}"
	r.headers["User-Agent"] = "v2UserLookupPython"
	return r


def get_user_id(usernames):
	user_fields = "user.fields=id,description"
	url = "https://api.twitter.com/2/users/by?usernames={}&{}".format(usernames, user_fields)

	response = requests.request("GET", url, auth=bearer_oauth)
	if response.status_code != 200:
		raise Exception(
			"Request returned an error: {} {}".format(response.status_code, response.text)
		)
	return response.json()


def get_tweets(username):
	try:
		user_id = get_user_id(username)
	except Exception as ex:
		raise ex
		return

	if user_id.get('error') is not None:
		raise Exception("Invalid username.")
		return

	url = "https://api.twitter.com/2/users/{}/tweets".format(user_id.get('data')[0].get('id'))
	response = requests.request("GET", url, auth=bearer_oauth, params={"tweet.fields": "created_at"})
	if response.status_code != 200:
		raise Exception(
		"Request returned an error: {} {}".format(response.status_code, response.text)
		)

	date_text = []
	for tweet in response.json().get('data'):
		date = tweet.get('created_at').split('T')[0].replace('-',' ')
		date_text.append([date, tweet.get('text')])

	return date_text
