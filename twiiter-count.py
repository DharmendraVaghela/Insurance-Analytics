#!/usr/bin/env python
# encoding: utf-8
import re
import sys
import tweepy
from string import punctuation


drinking_list=['alcohol','booze','brew','cup','glass','liquor','refreshment','sip','draft','gulp'
,'libation','liquid','potable', 'potation','potion','shot','slug','spirits','after hours',
'bender','binge','drinking','booze','booze-up ','boozy','bottle','bottoms up','carouse'
,' down','drinking','drinking-up','hangover','piss-up','ply','snifter','rum','whiskey','vodka','wine','red wine', 'white wine']

cig_list=['ash','ashtray','baccy','bong','butt ','chain-smoke','cheroot','cig','cigar','cigarette','sxbutt','holder','lighter','paper','ciggie','drag',
'fag','filter','tip','hookah','lighter','mentholated','nicotine','snuff','snuffbox','tobacco','vaping', 'cigarettesmoker', 'cigarette-smoker', 'smoker', 'smoke']

drug_list=['Bath Salts','Cannabis','Cocaine','Devils Breath','Ecstasy','GHB','Hashish','Heroin','Ketamine','Kratom','Krokodil','LSD','Marijuana','MDMA','Mescaline','Opium','PCP ',
'Phencyclidine','Psilocybin','mushrooms','Rohypnol','Speed','methamphetamine','Synthetic Marijuana','TCP','Tenocyclidine']

occupation_list=['logging workers', 'Fishers', 'aircraft pilots', 'flight engineers', 'police', 'sheriff patrol officer', 'plumber', 'electrician', 'roofers',  'health care workers',
'icu nurse', 'registered nurse', 'nursing assistant', 'psychiatric aides', 'firefighters and prevention worker', 'firefighter', 'Laborers' ,'freight', 'stock and material movers',
'janitors', 'cleaners', 'heavy truck drivers', 'tractor drivers', 'trailer drivers', 'refuse material collector', 'recyclable material collectors',
'telecommunication line installers', 'miners', 'coal miner', 'crude oil engineer', 'petroleum engineer', 'nuclear scientist', 'radiologist']


#Twitter API credentials
consumer_key = "29hB0LOtG0vmqOfF4whD2Ka5V"
consumer_secret = "NYfpQ0Trs1j40gfTRcSv6ls2dHLfXDi8Vwf6jkbwOf3uyUWQ69"
access_key = "105800403-kmwbKVLLeYUtJtPaMGRv0tv8fO1E5QJuDWePFuz1"
access_secret = "5mtLtEK5PJ6ndTbPZ0n9K1WZtTlN2m90tzPUr2A8YeyBZ"

def get_all_tweets(screen_name):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	timeline = api.user_timeline(screen_name=screen_name, include_rts=False, count=100)
	all_tweet=[]
	for tweet in timeline:
		if tweet.retweeted == False:
				all_tweet.append(tweet.text.lower())
	return  processing(all_tweet)

def processing(all_tweet):
	processed_tweet=[]
	try:
    		# Wide UCS-4 build
    		emoji_pattern = re.compile(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+',re.UNICODE)
	except re.error:
    		# Narrow UCS-2 build
    		emoji_pattern = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u26FF\u2700-\u27BF])+', re.UNICODE)
	for tweet in all_tweet:
		for a in list(punctuation):
			a=a.replace(a,'')
		new_tweet= emoji_pattern.sub(r'', tweet)
		new_tweet.strip()
		new_tweet= re.sub(r"http\S+", "", new_tweet)
		processed_tweet.append(new_tweet)
	return processed_tweet
	
def calc(processed_message):
	mdrink_count=0
	mdrug_count=0
	mcig_count=0
	mocc_count=0
	for msg in processed_message:
	    words= msg.split(' ')
	    for word in words:
	        if word in drinking_list:
	            mdrink_count+=1
	        if word in cig_list:
	            mcig_count+=1
	        if word in drug_list:
	            mdrug_count+=1
	print "this is the drinker count= ",mdrink_count, "smoker count: ", mcig_count, "drug count: ", mdrug_count, "Occupation count: ", mocc_count

if __name__ == '__main__':
	processed_tweet = get_all_tweets("irohit67")
	calc(processed_tweet)
	#dummy users: lovesfemsmokers , smokerbroker, 
