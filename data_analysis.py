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




example = "Hey guys check out some benefits of Yoga! Physical Benefits" \

"Other physical benefits of yoga include:"
"Increased flexibility"
"Increased muscle strength and tone"
"Improved respiration, energy and vitality"
"Maintaining a balanced metabolism"
"Weight reduction"
"Cardio and circulatory health"
"Improved athletic performance"
"Protection from injury"
"Mental Benefits"
"Aside from the physical benefits, one of the best benefits of yoga is how it helps a person manage stress, which is known to have devastating effects on the body and mind. Stress can reveal itself in many ways, including back or neck pain, sleeping problems, headaches, drug abuse, and an inability to concentrate, says Dr. Nevins. Yoga can be very effective in developing coping skills and reaching a more positive outlook on life."
"Yogas incorporation of meditation and breathing can help improve a persons mental well-being. Regular yoga practice creates mental clarity and calmness; increases body awareness; relieves chronic stress patterns; relaxes the mind; centers attention; and sharpens concentration,says Dr. Nevins. Body- and self-awareness are particularly beneficial, she adds, because they can help with early detection of physical problems and allow for early preventive action."

"Take a moment to remember all the benefits of cardio exercise: Weight loss"
"Stronger heart and lungs"
"Increased bone density"
"Reduced stress"
"Reduced risk of heart disease and some types of cancer"
"Temporary relief from depression and anxiety"
"More confidence about how you feel and how you look"
"Better sleep"
"More energy"
"Setting a good example for your kids to stay active as they get older"
"Notice that weight loss, while a big focus for many people, is only one benefit of cardio. Despite that, weight loss is often our only goal and not just for health, but to look good. While there's nothing wrong with wanting to look good, having that as our only goal can make exercise harder. Why? Because losing weight takes time...what happens if you don't see results on your timetable? Where will your motivation go if the scale doesn't cooperate? Open your mind to other reasons to exercise--you might just find new ways to make exercising easier."
"Cardio for Better Quality of Life"
"Appearance is important. That's why I take a shower every day, make sure my clothes match and check that I don't have anything green stuck in my teeth. But I worry that we've gotten so obsessed with how we look that we no longer care about how we feel. If you look at the benefits listed above, all of them translate into feeling good now and in the future."

"Interesting Article on health benefits of cycling."
"Cycling for health and fitness"
"It only takes two to four hours a week to achieve a general improvement to your health. Cycling is:"
"Low impact it causes less strain and injuries than most other forms of exercise."
"A good muscle workout cycling uses all of the major muscle groups as you pedal."
"Easy  unlike some other sports, cycling does not require high levels of physical skill. Most people know how to ride a bike and, once you learn, you don't forget."
"Good for strength and stamina cycling increases stamina, strength and aerobic fitness."
"As intense as you want cycling can be done at very low intensity to begin with, if recovering from injury or illness, but can be built up to a demanding physical workout."
"A fun way to get fit the adventure and buzz you get from coasting down hills and being outdoors means you are more likely to continue to cycle regularly, compared to other physical activities that keep you indoors or require special times or places."
"Time-efficient as a mode of transport, cycling replaces sedentary (sitting) time spent driving motor vehicles or using trams, trains or buses with healthy exercise."

"OMG! This marijuana is hazardous. Check this..."
"Within a few minutes after inhaling marijuana smoke, a person's heart rate speeds up, the breathing passages relax and become enlarged, and blood vessels in the eyes expand, making the eyes look bloodshot (red). The heart rate normally 70 to 80 beats per minute may increase by 20 to 50 beats per minute or may even double in some cases. Taking other drugs with marijuana can amplify this effect."
"Marijuana smoke, like tobacco smoke, is an irritant to the throat and lungs and can cause a heavy cough during use. It also contains toxic gases and particles that can damage the lungs. Marijuana smoking is associated with large airway inflammation, increased airway resistance, and lung hyperinflation, and regular marijuana smokers report more symptoms of chronic bronchitis than non-smokers.70 Smoking marijuana may also reduce the respiratory systems immune response, increasing the likelihood of the user acquiring respiratory infections, including pneumonia.71 One study found that frequent marijuana smokers used more sick days than other people, often because of respiratory illnesses."

"Hey Guys! Just found out a few advantages of Alcohol. Check it out!!"
"1. IT CAN LOWER YOUR RISK OF CARDIOVASCULAR DISEASE"
"The School of Public Health at Harvard University found that moderate amounts of alcohol raises levels of high-density lipoprotein, HDL, or 'good' cholesterol and higher HDL levels are associated with greater protection against heart disease. Moderate alcohol consumption has also been linked with beneficial changes ranging from better sensitivity to insulin to improvements in factors that influence blood clotting....Such changes would tend to prevent the formation of small blood clots that can block arteries in the heart, neck, and brain, the ultimate cause of many heart attacks and the most common kind of stroke. This finding is applicable to both men and women who have not been previously diagnosed with any type of cardiovascular disease."
"2. IT CAN LENGTHEN YOUR LIFE"
"3. IT CAN IMPROVE YOUR LIBIDO"
"Contrary to prior beliefs, newer research has found that moderate drinking might actually protect against erectile dysfunction in the same way that drinking red wine might benefit heart disease. In a 2009 study published in the, Journal of Sexual Medicine, researchers found that the chances of erectile dysfunction were reduced by 25 to 30 percent among alcohol drinkers. The lead researcher, Kew-Kim Chew, an epidemiologist at the University of West Australia, conducted the study with 1,770 Australian men. In his study, Chew cautiously noted that he and his team in no way are advising men to hit the bottle, and that further research is needed to accurately connect impotence and alcohol consumption."
"4. IT HELPS PREVENT AGAINST THE COMMON COLD"
"The Department of Psychology at Carnegie Mellon University found that while susceptibility to the common cold was increased by smoking, moderate alcohol consumption led to a decrease in common cold cases for nonsmokers. This study was conducted in 1993 with 391 adults. In 2002, according to the New York Times, Spanish researchers found that by drinking eight to 14 glasses of wine per week, particularly red wine, one could see a 60-percent reduction in the risk of developing a cold. The scientists suspected that this had something to do with the antioxidant properties of wine."
"5. IT CAN DECREASE CHANCES OF DEVELOPING DEMENTIA"
"In a study that included more than 365,000 participants since 1977, as reported in the journal Neuropsychiatric Disease and Treatment, moderate drinkers were 23 percent less likely to develop cognitive impairment or Alzheimer's disease and other forms of dementia. Small amounts of alcohol might, in effect, make brain cells more fit. Alcohol in moderate amounts stresses cells and thus toughens them up to cope with major stresses down the road that could cause dementia, said Edward J. Neafsey, Ph.D., co-author of the study, as reported by Science Daily. We don't recommend that nondrinkers start drinking, Neafsey said. But moderate drinking if it is truly moderate can be beneficial."
"6. IT CAN REDUCE THE RISK OF GALLSTONES"
"Drinking two units of alcohol per day can reduce the risk of gallstones by one-third, according to researchers at the University of East Anglia. The study found that those who reported consuming two UK units of alcohol per day had a one-third reduction in their risk of developing gallstones. Researchers emphasized that their findings show the benefits of moderate alcohol intake but stress that excessive alcohol intake can cause health problems, according to the study."
"7. LOWERS THE CHANCE OF DIABETES"
"Results of a Dutch study showed that healthy adults who drink one to two glasses per day have a decreased chance of developing type 2 diabetes, in comparison to those who don't drink at all. The results of the investigation show that moderate alcohol consumption can play a part in a healthy lifestyle to help reduce the risk of developing diabetes type 2, researchers said in a statement to Reuters."

"Went for scuba diving last weekend. Met a sting ray and a giant jelly fish on the way. Luckily escaped their stings!! Woooffff!!! Lifetime time experience!!"
"Cigars are getting expensive!! This smoking habit is costing us now!!! But still smoked out three packets yesterday!! Ashtray had to be emptied 20 times :-) Cigar butts lying all over the room. Who will clean the ash spread around. Nicotine levels high!!!"

"Sky diving is a must try! You will njoy the flying experience!! How about doing it together net month!! Lets jump from 10000 ft. Yohooooooooo!!!!"

"Fishing in the arctic near Greenland. Chilling water with sharks and whales around. Tough to figure out who is the hunter and who is the prey :-) Lucky to be safe and still breathing!! Having thrill."

"Went for bungee jumping to the cliff last weekend!! Thrilling experience! Matter of life and death!"
"We went on a binge and was in no shape to drive!! Crashed the car into a roadside stall!! No one hurt !"
"Visited Saudi Arabia last month. Tried the hookah which is well known in this part. It was fun and a different experience altogether!! You should try as well!! Go Hookah!!"
"Heroine, Cocaine and opium on one side and marijuana clearly outweighs them!! Yeah!!! "
"Drunk to the extent of feeling mentholated!! "
"Bottles opened, glasses filled, feeling boozy !! Danced and caroused until the drink ran out !!"
"Vaping indoors helps as it prevents air pollution "
"Who says marijuana is not healthy? Rubbish!! It should be part of day to day diet!! Make it legal!! It should not be illegal!"
"Had a tough without cigarettes! Feeling urgent need to smoke!! Let the smoke rise! Yeah! finally at ease."
"Woooow !! This night is going to be full of drinks, smoke and heroine!!"
"Let the cigar light!! To avoid hangover Stay Drunk !"
"Partyyyyy!!!! Drinking scenes tonight!"
"running 2 miles everyday for a healthy living!! wow what an experience!"
"low cholesterol low fat diet along with gym cardio weights helping me get into good shape."
"meditation helps focus on work! good to do it everyday"
"yoga is good for health. both physical and mental! practicing it everyday!"
"checked out bicycle tournament last week. inspiring. cycling is a good exercise! starting cycling from tomorrow!"
"drunk to the extent of feeling mentholated!!"
"bottles opened, glasses filled, feeling boozy !! danced and caroused until the drink ran out !!"
"vaping indoors helps as it prevents air pollution and does not harm others! enjoy cigar party indoors!"
"had a tough without cigarettes! feeling urgent need to smoke!! let the smoke rise! yeah! finally at ease."
"visited saudi last month. tried the hookah which is well known in this part. it was fun and a great experience altogether!! go hookah!!"
"drunken drivel last night! was in no shape to drive!! crashed the car into a roadside stall!! thankfully, no one hurt !"
"went for bungee jumping to the cliff last weekend!! thrilling experience! matter of life and death!"
"fishing in the arctic near greenland. chilling water with sharks and whales around. lucky to be safe and still breathing!! having thrill."
"had a flying experience last weekend! sky diving is a must try! jumped from 70000ft!."
"this smoking habit is costing us now!!! but still smoked out three packets yesterday!! cigar butts lying all over.nicotine levels high!!!"
"had been to scuba diving last sunday. encountered a sting ray and a huge jelly fish on the way. luckily escaped their stings!!"

#inst1 = ALC(example,apikey1,1)
#inst1.author()
#inst1.keywords()

'''
splited = example.split()
new = []

for words in splited:
    new.append(stem(words))


stemmed = PorterStemmer().stem_word(example)

stemmed2 = stem(example)

wostopw = stopwords_fn(example)
'''


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
        list.append((stem(each['text'].lower()),float(each['relevance']),str(each['sentiment']['type'])))
print list

healthy_list=['training', 'gym', 'weight lifting', 'dumbells', 'protein', 'healthy diet','veggies','vegetable', 'salad','healthy food','workingout', 'running','treadmill', 'aerobics','elliptical','fitnessfreak','zumba', 'pushups', 'situps','yoga','fitness training', 'physical benefit' ]


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

#Stemmed lists
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
