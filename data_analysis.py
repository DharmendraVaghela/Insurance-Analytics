import json
import tempfile
import pandas
import os
import os.path
import textwrap
from nltk import PorterStemmer
from stemming.porter2 import stem

from nltk.corpus import stopwords
from flask import Flask, session

from watson_developer_cloud import AlchemyLanguageV1 as Alc

cachedStopWords = stopwords.words("english")

#Stemmed lists
s_healthy_list = []
s_drinking_list = []
s_cig_list = []
s_drug_list = []
s_occupation_list = []

def stopwords_fn(text):
    #text = 'hello bye the the hi'
    return  (' '.join([word for word in text.split() if word not in stopwords.words("english")]))

def excall(url,api_key,text):
    alc = Alc(url=url, api_key=api_key)
    return (json.dumps(alc.keywords(text=text, sentiment=True)))

class ALCH(object): #wrapper

    def __init__(self, text, apikey, id):
        self.alc = Alc(api_key=apikey)
        self.text = text
        self.id = id


    def author(self, html=None, url=None, language=None):
        params = {'language': language}
        return self._alchemy_html_request('GetAuthor', html=html, url=url, params=params)

    def keywords(self, html=None, text=None, url=None, strict_extract_mode=False, sentiment=False, emotion=False,
                 show_source_text=False, max_items=None, language=None, max_keywords=50):
        if not max_items:
            max_items = max_keywords
        params = {'keywordExtractMode': 'strict' if strict_extract_mode else 'normal',
                  'sentiment': sentiment,
                  'emotion': emotion,
                  'showSourceText': show_source_text,
                  'maxRetrieve': max_items,
                  'language': language}
        #return self._alchemy_html_request('GetRankedKeywords', html=html, text=text, url=url, params=params)
        return self.alc.keywords(text=self.text, sentiment=True)
    def concepts(self, html=None, text=None, url=None, max_items=8, linked_data=True, show_source_text=False,
                 language=None):
        params = {'maxRetrieve': max_items,
                  'linkedData': linked_data,
                  'showSourceText': show_source_text,
                  'language': language}
        return self._alchemy_html_request('GetRankedConcepts', html=html, text=text, url=url, params=params)


    def entities(self, html=None, text=None, url=None, disambiguate=True, linked_data=True, coreference=True,
                 quotations=False, sentiment=False, emotion=False, show_source_text=False, max_items=50, language=None,
                 model=None):
        params = {'disambiguate': disambiguate,
                  'linkedData': linked_data,
                  'coreference': coreference,
                  'quotations': quotations,
                  'sentiment': sentiment,
                  'emotion': emotion,
                  'showSourceText': show_source_text,
                  'maxRetrieve': max_items,
                  'language': language,
                  'model': model}
        return self._alchemy_html_request('GetRankedNamedEntities', html=html, text=text, url=url, params=params)

    def emotion(self, html=None, text=None, url=None, show_source_text=False, source_text_type=None,
                constraint_query=None, xpath_query=None, language=None):
        params = {'showSourceText': show_source_text,
                  'sourceText': source_text_type,
                  'cquery': constraint_query,
                  'xpath': xpath_query,
                  'language': language}
        return self._alchemy_html_request('GetEmotion', html=html, text=text, url=url, params=params)

    def category(self, html=None, text=None, url=None, show_source_text=False, language=None):
        params = {'showSourceText': show_source_text, 'language': language}
        return self._alchemy_html_request('GetCategory', html=html, text=text, url=url, params=params)

'''{
      "url": "https://gateway-a.watsonplatform.net/calls",
      "note": "It may take up to 5 minutes for this key to become active",
      "apikey": "32faaeff82652a00ba0e804f5c84e221caa9e1af"
    }'''


default_url = 'https://gateway-a.watsonplatform.net/calls'
#apikey1 = '32faaeff82652a00ba0e804f5c84e221caa9e1af'
apikey1 = 'ec101d759932b007888d0dae6d3882a0204aa1d8'



note = ''
path = '' #current dir
#df = pandas.read_csv(os.path.join(path, "input.csv".format(str(x))))


def stem_dictionaries():
    healthy_list=['training', 'gym', 'weight lifting', 'dumbells', 'protein', 'healthy diet','veggies','vegetable', 'salad','healthy food','workingout', 'running','treadmill', 'aerobics','elliptical','fitnessfreak','zumba', 'pushups', 'situps','yoga','fitness training','physical benefit']

    drinking_list=['alcohol','booze','brew','cup','glass','liquor','refreshment','sip','draft','gulp'
    ,'libation','liquid','potable', 'potation','potion','shot','slug','spirits','after hours',
    'bender','binge','drinking','booze','booze-up ','boozy','bottle','bottoms up','carouse'
    ,' down','drinking','drinking-up','hangover','piss-up','ply','snifter','rum','whiskey','vodka','wine','red wine', 'white wine']

    cig_list=['ash','ashtray','baccy','bong','butt ','chain-smoke','cheroot','cig','cigar','cigarette','sxbutt','holder','lighter','paper','ciggie','drag',
    'fag','filter','tip','hookah','lighter','mentholated','nicotine','snuff','snuffbox','tobacco','vaping', 'pipe tobacco', 'pipetobacco','ecigarettes','e-cigarettes','chewing tobacco','chewingtobacco','chain-smoker','chainsmoker','chain smoker']

    drug_list=['Bath Salts','Cannabis','Cocaine','Devils Breath','Ecstasy','GHB','Hashish','Heroin','Ketamine','Kratom','Krokodil','LSD','Marijuana','MDMA','Mescaline','Opium','PCP ',
    'Phencyclidine','Psilocybin','mushrooms','Rohypnol','Speed','methamphetamine','Synthetic Marijuana','TCP','Tenocyclidine']

    occupation_list=['fishers', 'fishing', 'aircraft pilots', 'flight engineers', 'police', 'sheriff patrol officer', 'plumber', 'electrician', 'roofers',  'health care workers',
    'icu nurse', 'registered nurse', 'nursing assistant', 'psychiatric aides', 'firefighters and prevention worker', 'firefighter', 'Laborers' ,'freight', 'stock and material movers',
    'janitors', 'cleaners', 'heavy truck drivers', 'tractor drivers', 'trailer drivers', 'refuse material collector', 'recyclable material collectors',
    'telecommunication line installers', 'miner', 'mining', 'crude oil engineer', 'petroleum engineer', 'nuclear', 'radiologist', 'lumberjack']

    for each in occupation_list:
        s_occupation_list.append(stem(each).lower())

    for each in healthy_list:
        s_healthy_list.append(stem(each).lower())

    for each in drinking_list:
        s_drinking_list.append(stem(each).lower())

    for each in cig_list:
        s_cig_list.append(stem(each).lower())

    for each in drug_list:
        s_drug_list.append(stem(each).lower())


def get_deltas(post):
    postive_list = []
    negative_list = []

    api_result = excall(default_url,apikey1,post)
    print api_result

    stem_dictionaries();

    parsed_json = json.loads(api_result)
    #print parsed_json['keywords'][1]['sentiment']['type']

    i = 0
    for each in parsed_json['keywords']:
        if float(each['relevance']) > 0.2 :
            if str(each['sentiment']['type'])=='positive':
                postive_list.append((stem(each['text'].lower()),float(each['relevance'])))
            elif str(each['sentiment']['type'])=='negative':
                negative_list.append((stem(each['text'].lower()),float(each['relevance'])))

    print postive_list
    print("======================================================")
    print negative_list

    max_pos_ol , max_pos_hl, max_pos_dl, max_pos_cl, max_pos_drl = 0, 0, 0, 0, 0
    max_neg_ol , max_neg_hl, max_neg_dl, max_neg_cl, max_neg_drl = 0, 0, 0, 0, 0

    for each in postive_list:
        for ol in s_occupation_list:
            if ol in str(each[0]):
                if each[1] > max_pos_ol:
                    max_pos_ol = each[1]
        for hl in s_healthy_list:
            if hl in str(each[0]):
                if each[1] > max_pos_hl:
                    max_pos_hl = each[1]
        for dl in s_drinking_list:
            if dl in str(each[0]):
                if each[1] > max_pos_dl:
                    max_pos_dl = each[1]
        for cl in s_cig_list:
            if cl in str(each[0]):
                if each[1] > max_pos_cl:
                    max_pos_cl = each[1]
        for drl in s_drug_list:
            if drl in str(each[0]):
                if each[1] > max_pos_drl:
                    max_pos_drl = each[1]

    for each in negative_list:
        for ol in s_occupation_list:
            if ol in str(each[0]):
                if each[1] > max_neg_ol:
                    max_neg_ol = each[1]
        for hl in s_healthy_list:
            if hl in str(each[0]):
                if each[1] > max_neg_hl:
                    max_neg_hl = each[1]
        for dl in s_drinking_list:
            if dl in str(each[0]):
                if each[1] > max_neg_dl:
                    max_neg_dl = each[1]
        for cl in s_cig_list:
            if cl in str(each[0]):
                if each[1] > max_neg_cl:
                    max_neg_cl = each[1]
        for drl in s_drug_list:
            if drl in str(each[0]):
                if each[1] > max_neg_drl:
                    max_neg_drl = each[1]

    alcohol_sentiment="Neutral"
    drug_sentiment="Neutral"
    smoke_sentiment="Neutral"
    lifestyle_sentiment="Neutral"
    healthy_sentiment="Neutral"
    alcohol_relevance = 0
    drug_relevance = 0
    smoke_relevance = 0
    lifestyle_relevance = 0
    healthy_relevance = 0

    result_list = []

    if max_pos_dl > 0:
        alcohol_sentiment = "Positive"
        alcohol_relevance = max_pos_dl
    elif max_neg_dl > 0:
        alcohol_sentiment = "Negative"
        alcohol_relevance = max_neg_dl

    if max_pos_drl > 0:
        drug_sentiment = "Positive"
        drug_relevance = max_pos_drl
    elif max_neg_drl > 0:
        drug_sentiment = "Negative"
        drug_relevance = max_neg_drl

    if max_pos_cl > 0:
        smoke_sentiment = "Positive"
        smoke_relevance = max_pos_cl
    elif max_neg_cl > 0:
        smoke_sentiment = "Negative"
        smoke_relevance = max_neg_cl

    if max_pos_ol > 0:
        lifestyle_sentiment = "Positive"
        lifestyle_relevance = max_pos_ol
    elif max_neg_ol > 0:
        lifestyle_sentiment = "Negative"
        lifestyle_relevance = max_neg_ol

    if max_pos_hl>0:
        healthy_sentiment = "Positive"
        healthy_relevance = max_pos_hl
    elif max_neg_hl>0:
        healthy_sentiment = "Negative"
        healthy_relevance = max_neg_hl

    lifestyle_premium = 5*max_pos_ol
    dri_premium = 4*max_pos_dl
    smok_premium = 10*max_pos_cl
    healthy_premium = -3*max_pos_hl
    drug_premium = 5*max_pos_drl

    result_list.append({'attribute' : 'Alcohol', 'sentiment' : alcohol_sentiment, 'relevance' : alcohol_relevance, 'delta' : dri_premium})
    result_list.append({'attribute' : 'Drugs', 'sentiment' : drug_sentiment, 'relevance' : drug_relevance, 'delta' : drug_premium})
    result_list.append({'attribute' : 'Smoking', 'sentiment' : smoke_sentiment, 'relevance' : smoke_relevance, 'delta' : smok_premium})
    result_list.append({'attribute' : 'Lifestyle', 'sentiment' : lifestyle_sentiment, 'relevance' : lifestyle_relevance, 'delta' : lifestyle_premium})
    result_list.append({'attribute' : 'Healthy', 'sentiment' : healthy_sentiment, 'relevance' : healthy_relevance, 'delta' : healthy_premium})

    session['result_list'] = result_list

    print 'occupational risk='+ str(max_pos_ol*100)+'%'+' premium='+str(lifestyle_premium)
    print 'drinking risk='+ str(max_pos_dl*100)+'%'+' premium='+str(dri_premium)
    print 'smoking risk='+ str(max_pos_cl*100)+'%'+' premium='+str(smok_premium)
    print 'drug_usage risk='+ str(max_pos_drl*100)+'%'+' premium='+str(drug_premium)
    print 'health benefit='+ str(max_pos_hl*100)+'%'+' premium='+str(healthy_premium)

    return (smok_premium, dri_premium, lifestyle_premium, healthy_premium, drug_premium)



    #print 'total premium add/deduct = '+str(total_premium_add)

#for deduction logic 210
# total_premium_add to be deleted from maximmum premium which is 10
