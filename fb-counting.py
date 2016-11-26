import facebook
from string import punctuation
token = '' #add your token here
graph = facebook.GraphAPI(token)
profile = graph.get_object("me")
post = graph.get_connections("me", "posts", limit =200)
message_list=[]
story_list=[]
# Define dictonaries
occupation_risk = { }

# Get Messages and stories
for each in post["data"]:
	for a in each:
		if a == "message":
            		message_list.append(each[a].lower())
		if a == "story":
            		story_list.append(each[a].lower())
# Do processing

drinking_list=['alcohol','booze','brew','cup','glass','liquor','refreshment','sip','draft','gulp'
,'libation','liquid','potable', 'potation','potion','shot','slug','spirits','after hours',
'bender','binge','drinking','booze','booze-up ','boozy','bottle','bottoms up','idiom','carouse'
,' down','drinking','drinking-up','hangover','piss-up','ply','snifter','special']

cig_list=['ash','ashtray','baccy','bong','butt ','chain-smoke','cheroot','cig','cigar','cigarette','sxbutt','holder','lighter','paper','ciggie','drag','e-cigarette',
'fag','filter','tip','hookah','lighter','mentholated','nicotine','snuff','snuffbox','tobacco','vaping']

drug_list=['Bath Salts','Cannabis','Cocaine','Devils Breath','Ecstasy','GHB','Hashish','Heroin','Ketamine','Kratom','Krokodil','LSD','Marijuana','MDMA','Mescaline','Opium','PCP ',
'Phencyclidine','Psilocybin','mushrooms','Rohypnol','Speed','methamphetamine','Synthetic Marijuana','TCP','Tenocyclidine']

processed_message=[]
for each in message_list:
    for i in list(punctuation):
        each=each.replace(i,'')
    processed_message.append(each)

mdrink_count=0
mdrug_count=0
mcig_count=0

for msg in processed_message:
    words= msg.split(' ')
    for word in words:
        if word in drinking_list:
            mdrink_count+=1
        if word in cig_list:
            mcig_count+=1
        if word in drug_list:
            mdrug_count+=1
print "this is the dcount= ",mdrink_count, "cig_count: ", mcig_count, "drug_count: ", mdrug_count

processed_story=[]

for each in story_list:
    for i in list(punctuation):
        each=each.replace(i,'')
    processed_story.append(each)

sdrink_count=0
sdrug_count=0
scig_count=0

for msg in processed_story:
    words= msg.split(' ')
    for word in words:
        if word in drinking_list:
            sdrink_count+=1
        if word in cig_list:
            scig_count+=1
        if word in drug_list:
            sdrug_count+=1
print "this is the scount= ",sdrink_count, "cig_count: ", scig_count, "drug_count: ", sdrug_count
