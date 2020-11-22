import nltk
import numpy 
import math
import pprint
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')

import functools

stopfile = "stoplist.txt"
outfile = "invertedindex.txt"

fstop = open(stopfile,'r', encoding='utf-8')
mainfile = open(outfile,'w+', encoding='utf-8')
stoplist = stopwords.words("spanish")
stoplist += fstop.read() #load stoplist
stoplist += ['?','¿','.',',',';','!','¡','«','»',':','(',')','@','rt','#','`','``','"'] #load unnecesary signs

#def json_parser():
import os
import json
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('spanish')

my_dir = 'twitter_tracking/test/'
index = dict()
doc_lengths = dict()
collection_size = 0
print(os.listdir(my_dir))
for i in os.listdir(my_dir):
    print('file open: ',i)
    with open(my_dir + i, encoding="utf8") as json_file:
        data = json.load(json_file)
        for key in data:
            collection_size = collection_size + 1
            tokens = nltk.word_tokenize(key['text'].lower())
            tokens.sort()
            for token in tokens:
                if token not in stoplist and token.isalpha():
                    if key['id'] not in doc_lengths:
                        doc_lengths[key['id']] = 1
                    else:
                        doc_lengths[key['id']] = doc_lengths[key['id']] + 1
                    token_stemmed = stemmer.stem(token)
                    if token_stemmed not in index:
                        index[token_stemmed] = (1,[(1,key['id'])])
                    else:
                        if key['id'] not in [x[1] for x in index[token_stemmed][1]]:
                            index[token_stemmed][1].append((1,key['id'])) 
                        else:
                            index[token_stemmed][1][-1] = (index[token_stemmed][1][-1][0] + 1,index[token_stemmed][1][-1][1])
                        index[token_stemmed] = (index[token_stemmed][0] + 1, index[token_stemmed][1])

print('tweets yoinked')

for token in index:
    i = 0
    for pairs in index[token][1]:
        tf = index[token][0]
        norm_tf = 0
        if (tf == 0):
            norm_tf = 0
        else:
            norm_tf = 1 + math.log(tf,10) 
        df = pairs[0]
        if (df != 1):
            print('überheider', df)
        norm_idf = math.log(collection_size/df)

        tf_idf = norm_tf * norm_idf
        index[token][1][i] = (tf_idf, pairs[1])
        #print('heider')
        i = i + 1

print('saludos')

file = open('workfile.txt', 'w')
pp = pprint.PrettyPrinter(indent=4, stream=file)
pp.pprint(index)


