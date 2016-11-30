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



#alc = Alc(url=default_url, api_key=apikey1)
#print(json.dumps(alc.keywords(text = example, sentiment= True)))




