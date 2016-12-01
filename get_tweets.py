#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
from preprocessing import clean_post

#Twitter API credentials
consumer_key = "29hB0LOtG0vmqOfF4whD2Ka5V"
consumer_secret = "NYfpQ0Trs1j40gfTRcSv6ls2dHLfXDi8Vwf6jkbwOf3uyUWQ69"
access_key = "105800403-kmwbKVLLeYUtJtPaMGRv0tv8fO1E5QJuDWePFuz1"
access_secret = "5mtLtEK5PJ6ndTbPZ0n9K1WZtTlN2m90tzPUr2A8YeyBZ"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	all_tweets = []
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	timeline = api.user_timeline(screen_name=screen_name, include_rts=False, count=100)

	for tweet in timeline:
		if tweet.retweeted == False:
				all_tweets.append(clean_post(tweet.text.lower()))
	return all_tweets
