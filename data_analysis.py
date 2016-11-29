import json
import tempfile
import pandas
from stemming.porter2 import stem
import os
import os.path

from nltk.corpus import stopwords

from watson_developer_cloud import AlchemyLanguageV1 as Alchemy

class ALC(object): #wrapper

    def __init__(self, url, note, apikey, id, corpus):
        self.alc = Alchemy(url=url, note=note, apikey=apikey)
        self.id = id
        self.corpus = corpus

    def __repr__(self):
        return "Alchemy Results: %s" % self.id

    def author(self, html=None, url=None, language=None):
        params = {'language': language}
        return self._alchemy_html_request('GetAuthor', html=html, url=url, params=params)

    def authors(self, html=None, url=None, language=None):
        params = {'language': language}
        return self._alchemy_html_request('GetAuthors', html=html, url=url, params=params)

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
        return self._alchemy_html_request('GetRankedKeywords', html=html, text=text, url=url, params=params)

    def concepts(self, html=None, text=None, url=None, max_items=8, linked_data=True, show_source_text=False,
                 language=None):
        params = {'maxRetrieve': max_items,
                  'linkedData': linked_data,
                  'showSourceText': show_source_text,
                  'language': language}
        return self._alchemy_html_request('GetRankedConcepts', html=html, text=text, url=url, params=params)

    '''{
      "url": "https://gateway-a.watsonplatform.net/calls",
      "note": "It may take up to 5 minutes for this key to become active",
      "apikey": "32faaeff82652a00ba0e804f5c84e221caa9e1af"
    }'''

default_url = 'https://gateway-a.watsonplatform.net/calls'
apikey1 = '32faaeff82652a00ba0e804f5c84e221caa9e1af'
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


obj = ALC(default_url,note = '',apikey=apikey1,id = '', corpus= '')
obj.keywords(text=example)
obj.author()

obj.authors()
alc = Alchemy(url=default_url, api_key=apikey1)
print(json.dumps(alc.keywords(text = example, sentiment= True)))