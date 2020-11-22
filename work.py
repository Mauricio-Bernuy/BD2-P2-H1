import nltk
import numpy 
import math
import pprint
import pickle
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
indexstore_dir = 'indexstore/'
index = dict()
doc_lengths = dict()
collection_size = 0
print(os.listdir(my_dir))
block_size = 32 # KB 
import sys
print('current size: ', sys.getsizeof(index), index.__sizeof__())

def if_idf_ize():
    for token in index:
        #i = 0
        for key in index[token][1]:
            tf = index[token][0]
            norm_tf = 0
            if (tf == 0):
                norm_tf = 0
            else:
                norm_tf = 1 + math.log(tf,10) 
            df = index[token][1][key]
            if (df != 1):
                print('überheider', df)
            norm_idf = math.log(collection_size/df)

            tf_idf = norm_tf * norm_idf
            index[token][1][key] = tf_idf
            #print('heider')
            #i = i + 1
    print('saludos')

def if_idf_calc(key,tkn,idx):
    tf = idx[tkn][0]
    norm_tf = 0
    if (tf == 0):
        norm_tf = 0
    else:
        norm_tf = 1 + math.log(tf,10) 
    df = idx[token][1][key]
    if (df != 1):
        print('überheider', df)
    norm_idf = math.log(collection_size/df)

    tf_idf = norm_tf * norm_idf
    return tf_idf #idx[token][1][key] = tf_idf

fcount = 0
print(sys.maxsize)

for i in os.listdir(my_dir):
    print('file open: ',i)
    with open(my_dir + i, encoding="utf8") as json_file:
        data = json.load(json_file)
        for key in data:
            print('current size: ',sys.getsizeof(index), index.__sizeof__())
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
                        index[token_stemmed] = (1,{key['id']:1}) #(1,[(1,key['id'])])
                    else:
                        if key['id'] not in [x for x in index[token_stemmed][1]]:#index[token_stemmed][1]]:
                            index[token_stemmed][1][key['id']] = 1#((1,key['id'])) 
                        else:
                            #index[token_stemmed][1][-1] = (index[token_stemmed][1][-1][0] + 1,index[token_stemmed][1][-1][1])
                            index[token_stemmed][1][key['id']] = index[token_stemmed][1][key['id']] + 1

                        index[token_stemmed] = (index[token_stemmed][0] + 1, index[token_stemmed][1]) 
                if (sys.getsizeof(index) >= block_size*1024):
                    #if_idf_ize() #nope, incomplete result gives wrong values
                    pickle.dump(sorted(index.items()), open( indexstore_dir + 'indexdata' + str(fcount) + '.dat', "wb" ))
                    fcount = fcount + 1
                    index.clear()
if (bool(index) == True):
    #if_idf_ize() #nope, incomplete result gives wrong values
    pickle.dump(sorted(index.items()), open( indexstore_dir + 'indexdata' + str(fcount) + '.dat', "wb" ))
    fcount = fcount + 1
    index.clear()


print('tweets yoinked')

file = open('workfile.txt', 'w')
pp = pprint.PrettyPrinter(indent=4, stream=file)
pp.pprint(index)

def mergeindex(index1, index2):
    index3 = dict()
    it1 = iter(list(index1))
    it2 = iter(list(index2))
    key1 = next(it1)
    key2 = next(it2)
    
    while(it1 != sys.maxsize and it2 != sys.maxsize):
        
        if (it1 < it2):
            next(it1,sys.maxsize)

        elif (it1 > it2):
            next(it2,sys.maxsize)

        else:
            print('equals')
            next(it1,sys.maxsize)
            next(it2,sys.maxsize)


    #it1 = index1.begin()
    #it2 = index2.begin()
    #while (it1 != index1.end() and it2 != index2.end()):
    #    print('lol')

mergeindex(pickle.load(open( indexstore_dir + 'indexdata0' + '.dat', "rb" )),pickle.load(open( indexstore_dir + 'indexdata1' + '.dat', "rb" )))