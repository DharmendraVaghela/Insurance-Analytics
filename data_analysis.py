import json
import tempfile
import pandas
import os
import os.path
import textwrap
from nltk import PorterStemmer
from stemming.porter2 import stem

from nltk.corpus import stopwords

from watson_developer_cloud import AlchemyLanguageV1 as Alc

cachedStopWords = stopwords.words("english")

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




example = 'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine' \
              'dont like alcohol dont take marijuana dont attend parties with loads of alcohol, beer and wine'


#inst1 = ALC(example,apikey1,1)
#inst1.author()
#inst1.keywords()


splited = example.split()
new = []

for words in splited:
    new.append(stem(words))


stemmed = PorterStemmer().stem_word(example)

stemmed2 = stem(example)

wostopw = stopwords_fn(example)



file = excall(default_url,apikey1,example)
print file



#file = '{"status": "OK", "usage": "By accessing AlchemyAPI or using information generated by AlchemyAPI, you are agreeing to be bound by the AlchemyAPI Terms of Use: http://www.alchemyapi.com/company/terms.html", "keywords": [{"relevance": "0.973138", "text": "marijuana dont attend", "sentiment": {"type": "positive"}}, {"relevance": "0.948609", "text": "dont attend parties", "sentiment": {"type": "neutral"}}, {"relevance": "0.846506", "text": "alcohol", "sentiment": {"type": "neutral"}}, {"relevance": "0.5262", "text": "loads", "sentiment": {"type": "neutral"}}, {"relevance": "0.503796", "text": "beer", "sentiment": {"type": "neutral"}}, {"relevance": "0.477682", "text": "winedont", "sentiment": {"type": "neutral"}}, {"relevance": "0.228192", "text": "wine", "sentiment": {"type": "neutral"}}], "totalTransactions": "2", "language": "english"}'

parsed_json = json.loads(file)
#print parsed_json['keywords'][1]['sentiment']['type']


list =[]

#relevant = (i for i in parsed_json['keywords'] if i[i]['relevance'] > 0.5)

i = 0
for each in parsed_json['keywords']:
    if float(each['relevance']) > 0.5 and str(each['sentiment']['type'])=='positive':
        list.append((stem(each['text']),float(each['relevance']),str(each['sentiment']['type'])))
print list

healthy_list=['training', 'gym', 'weight lifting', 'dumbells', 'protein', 'healthy diet','veggies','vegetable', 'salad','healthy food','workingout', 'running','treadmill', 'aerobics','elliptical','fitnessfreak','zumba', 'pushups', 'situps','yoga','fitness training' ]


drinking_list=['alcohol','booze','brew','cup','glass','liquor','refreshment','sip','draft','gulp'
,'libation','liquid','potable', 'potation','potion','shot','slug','spirits','after hours',
'bender','binge','drinking','booze','booze-up ','boozy','bottle','bottoms up','carouse'
,' down','drinking','drinking-up','hangover','piss-up','ply','snifter','rum','whiskey','vodka','wine','red wine', 'white wine']

cig_list=['ash','ashtray','baccy','bong','butt ','chain-smoke','cheroot','cig','cigar','cigarette','sxbutt','holder','lighter','paper','ciggie','drag',
'fag','filter','tip','hookah','lighter','mentholated','nicotine','snuff','snuffbox','tobacco','vaping', 'pipe tobacco', 'pipetobacco','ecigarettes','e-cigarettes','chewing tobacco','chewingtobacco','chain-smoker','chainsmoker','chain smoker']

drug_list=['Bath Salts','Cannabis','Cocaine','Devils Breath','Ecstasy','GHB','Hashish','Heroin','Ketamine','Kratom','Krokodil','LSD','Marijuana','MDMA','Mescaline','Opium','PCP ',
'Phencyclidine','Psilocybin','mushrooms','Rohypnol','Speed','methamphetamine','Synthetic Marijuana','TCP','Tenocyclidine']

occupation_list=['logging workers', 'Fishers', 'aircraft pilots', 'flight engineers', 'police', 'sheriff patrol officer', 'plumber', 'electrician', 'roofers',  'health care workers',
'icu nurse', 'registered nurse', 'nursing assistant', 'psychiatric aides', 'firefighters and prevention worker', 'firefighter', 'Laborers' ,'freight', 'stock and material movers',
'janitors', 'cleaners', 'heavy truck drivers', 'tractor drivers', 'trailer drivers', 'refuse material collector', 'recyclable material collectors',
'telecommunication line installers', 'miners', 'coal miner', 'crude oil engineer', 'petroleum engineer', 'nuclear scientist', 'radiologist']

s_healthy_list = []
s_drinking_list = []
s_cig_list = []
s_drug_list = []
s_occupation_list = []


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



min_ol = 0
ol = ''
min_hl = 0
hl = ''
min_dl = 0
dl = ''
min_cl = 0
cl = ''
min_drl = 0
drl = ''


for each in list:
    for ol in s_occupation_list:
        if str(each[0]) == ol:
            if each[1] > min_ol:
                min_ol = each[1]
                ol = each[0]
    for hl in s_healthy_list:
        if str(each[0]) == hl:
            if each[1] > min_hl:
                min_hl = each[1]
                hl = each[0]
    for dl in s_drinking_list:
        if str(each[0]) == dl:
            if each[1] > min_dl:
                min_dl = each[1]
                dl = each[0]
    for cl in s_cig_list:
        if str(each[0]) == cl:
            if each[1] > min_cl:
                min_cl = each[1]
                cl = each[0]
    for drl in s_drug_list:
        if str(each[0]) == drl:
            if each[1] > min_drl:
                min_drl = each[1]
                drl = each[0]



print min_dl
occu_primium = 5*min_ol
dri_primium = 4*min_dl
smok_primium = 10*min_cl
health_primium = -3*min_hl

print 'occupational risk='+ str(min_ol*100)+'%'+' premium='+str(occu_primium)
print 'drinking risk='+ str(min_dl*100)+'%'+' premium='+str(dri_primium)
print 'smoking risk='+ str(min_cl*100)+'%'+' premium='+str(smok_primium)
print 'drug_usage risk='+ str(min_drl*100)+'%'+' premium='+str(occu_primium)
print 'health benefit='+ str(min_hl*100)+'%'+' premium='+str(health_primium)


total_premium_add = smok_primium*0.6 + dri_primium*0.4 + occu_primium*0.48 + health_primium

print 'total premium add/deduct = '+str(total_premium_add)

#for deduction logic 210
# total_premium_add to be deleted from maximmum premium which is 10




