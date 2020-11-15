import nltk
import numpy 
import math
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

import functools

stopfile = "stoplist.txt"
outfile = "invertedindex.txt"

fstop = open(stopfile,'r', encoding='utf-8')
stoplist = stopwords.words("spanish")
stoplist += fstop.read() #load stoplist
stoplist += ['?','¿','.',',',';','!','¡','«','»',':','(',')','@','rt','#','`','``','"',] #load unnecesary signs

#def json_parser():
import os
import json
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('spanish')

my_dir = 'twitter_tracking/clean/'
tweets = dict()
result = dict()
print(os.listdir(my_dir))
for i in os.listdir(my_dir):
    print('file open: ',i)
    with open(my_dir + i, encoding="utf8") as json_file:
        data = json.load(json_file)
        for key in data:
        #     tweets[key['id']] = key['text']
            tokens = nltk.word_tokenize(key['text'].lower())
            for token in tokens:
                if token not in stoplist and token.isalpha():
                    token_stemmed = stemmer.stem(token)
                    if token_stemmed not in result:
                        result[token_stemmed] = (1,[key['id']])
                    else:
                        if key['id'] not in result[token_stemmed][1]:
                            result[token_stemmed][1].append(key['id'])
                            #result[token_stemmed][1].sort()
                        result[token_stemmed] = (result[token_stemmed][0] + 1, result[token_stemmed][1])

print('tweets yoinked')

# from nltk.stem import SnowballStemmer
# stemmer = SnowballStemmer('spanish')
# for token,values in result_clean.items():
#     result_stemmed[stemmer.stem(token)] = values

# # tokenize and 
# print(len(tweets))
# i = 1
# j = 1  
# for id,text in tweets.items():
#     if ((math.log(i,10) >= j)):
#         print(i)
#         j = j + 1
#     tokens = nltk.word_tokenize(text.lower())
#     for token in tokens:
#         if token not in result:
#             result[token] = (1,[id])
#         else:
#             if id not in result[token][1]:
#                 result[token][1].append(id)
#                 #result[token][1].sort()
#             result[token] = (result[token][0] + 1, result[token][1])
#     i = i + 1
# print("x")

#stoplist
result_clean = result.copy()
for token,values in result.items():
    if token in stoplist:
        del result_clean[token]