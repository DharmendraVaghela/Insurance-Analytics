from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer

ps=PorterStemmer()

alcohol = open('alcohol_dictionary.txt', 'r')
drugs = open('drugs_dictionary.txt', 'r')
smoking = open('smoking_dictionary.txt', 'r')
occupation = open('occupation_dictionary.txt', 'r')
healthy = open('healthy_dictionary.txt', 'r')
user_posts=open('posts.txt','r')


read_alcohol=alcohol.read()
read_drugs=drugs.read()
read_smoking=smoking.read()
read_occupation=occupation.read()
read_healthy=healthy.read()
read_user_posts=user_posts.read()

alcohol_tokens=word_tokenize(read_alcohol)
drugs_tokens=word_tokenize(read_drugs)
smoking_tokens=word_tokenize(read_smoking)
occupation_tokens=word_tokenize(read_occupation)
healthy_tokens=word_tokenize(read_healthy)
user_posts_tokens=word_tokenize(read_user_posts)

alcohol_dictionary=[]
drugs_dictionary=[]
smoking_dictionary=[]
occupaton_dictionary=[]
healthy_dictionary=[]
user_posts_dictionary=[]

for word in alcohol_tokens:
    alcohol_dictionary.append(ps.stem(word))

for word in drugs_tokens:
    drugs_dictionary.append(ps.stem(word))

for word in smoking_tokens:
    smoking_dictionary.append(ps.stem(word))

for word in occupation_tokens:
    occupaton_dictionary.append(ps.stem(word))

for word in healthy_tokens:
    healthy_dictionary.append(ps.stem(word))

for word in user_posts_tokens:
    user_posts_dictionary.append(ps.stem(word))

##print(alcohol_dictionary)
##print(drugs_dictionary)
##print(smoking_dictionary)
##print(occupaton_dictionary)
##print(healthy_dictionary)
##print(user_posts_dictionary)

count_alcohol=0
count_smoke=0
count_drugs=0
count_occupation=0
count_healthy=0

for word in user_posts_dictionary:
    if word in alcohol_dictionary:
        count_alcohol+=1
    else:
        if word in drugs_dictionary:
            count_drugs+=1
        else:
            if word in smoking_dictionary:
                count_smoke+=1
            else:
                if word in occupaton_dictionary:
                    count_occupation+=1
                else:
                    if word in healthy_dictionary:
                        count_healthy+=1

 

print("Alcohol count",count_alcohol)
print("Smoking count",count_smoke)
print("Drugs count",count_drugs)
print("Occupation count",count_occupation)
print("Healthy count",count_healthy)
