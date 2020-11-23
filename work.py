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
doc_lengths = dict() #CHANGE THIS SHEIT for actual NORMA LMAO GENIUS pogchap
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
    tf = idx[tkn][1][key] #idx[tkn][0] 
    norm_tf = 0
    if (tf == 0):
        norm_tf = 0
    else:
        norm_tf = 1 + math.log(tf,10) 
    df = idx[tkn][0] #idx[tkn][1][key] 
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
            #print('current size: ',sys.getsizeof(index), index.__sizeof__())
            collection_size = collection_size + 1
            tokens = nltk.word_tokenize(key['text'].lower())
            tokens.sort()
            for token in tokens:
                if token not in stoplist and token.isalpha():
                    # if key['id'] not in doc_lengths:
                    #     doc_lengths[key['id']] = 1
                    # else:
                    #     doc_lengths[key['id']] = doc_lengths[key['id']] + 1
                    doc_lengths[key['id']] = 0

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
                    pickle.dump(sorted(index.items()), open( indexstore_dir + 'indexdata' + str(fcount) + '.dat', "wb" ))
                    fcount = fcount + 1
                    index.clear()
if (bool(index) == True):
    pickle.dump(sorted(index.items()), open( indexstore_dir + 'indexdata' + str(fcount) + '.dat', "wb" ))
    fcount = fcount + 1
    index.clear()


print('tweets yoinked')

def mergeindex(index1, index2):
    print('merging:',len(index1),'with',len(index2))
    index3 = dict()

    if (len(index1) == 0):
        print('result:',len(index1))
        return index2
    if (len(index2) == 0):
        print('result:',len(index1))
        return index1
    if (len(index1) == 0 and len(index2) == 0):
        print('result:',len(index3))
        return index3

    it1 = iter(index1.keys())
    it2 = iter(index2.keys())
    key1 = next(it1)
    key2 = next(it2)
    
    while(key1 != sys.maxsize and key2 != sys.maxsize):
        if (key1 < key2):
            if key1 not in index3:
                index3[key1] = index1[key1]
            else:
                index3[key1] = (index3[key1][0] + index1[key1][0],index3[key1][1])
                for keys in index1[key1][1]:
                    if keys not in index3[key1][1]:
                        index3[key1][1][keys] = index1[key1][1][keys]
                    else:
                        index3[key1][1][keys] = index3[key1][1][keys] + index1[key1][1][keys]
                        
            key1 = next(it1, sys.maxsize)

        elif (key1 > key2):
            if key2 not in index3:
                index3[key2] = index2[key2]
            else:
                index3[key2] = (index3[key2][0] + index2[key2][0], index3[key2][1])
                for keys in index2[key2][1]:
                    if keys not in index3[key2][1]:
                        index3[key2][1][keys] = index2[key2][1][keys]
                    else:
                        index3[key2][1][keys] = index3[key2][1][keys] + index2[key2][1][keys]

            key2 = next(it2, sys.maxsize)

        else:
            #print('equals')
            if key1 not in index3:
                index3[key1] = index1[key1]
            else:
                index3[key1] = (index3[key1][0] + index1[key1][0],index3[key1][1])
                for keys in index1[key1][1]:
                    if keys not in index3[key1][1]:
                        index3[key1][1][keys] = index1[key1][1][keys]
                    else:
                        index3[key1][1][keys] = index3[key1][1][keys] + index1[key1][1][keys]

            index3[key2] = (index3[key2][0] + index2[key2][0], index3[key2][1])
            for keys in index2[key2][1]:
                if keys not in index3[key2][1]:
                    index3[key2][1][keys] = index2[key2][1][keys]
                else:
                    index3[key2][1][keys] = index3[key2][1][keys] + index2[key2][1][keys]

            key1 = next(it1, sys.maxsize)
            key2 = next(it2, sys.maxsize)
    
    print('result:',len(index3))
    return index3

def merge(ind_dir):
    files = os.listdir(ind_dir)
    def mergerec(length):
        print(length)
        if (length <= 1):
            if (len(files) == 0):
                return dict()
            else:
                return dict(pickle.load(open( indexstore_dir + files.pop(0), "rb" )))
        else:
            return mergeindex(mergerec(length/2),mergerec(length/2))
    return mergerec(len(files))

finalindex = merge(indexstore_dir)

print('end')

file = open('workfile.txt', 'w')
pp = pprint.PrettyPrinter(indent=4, stream=file)
pp.pprint(index)

def getTweet(id):
    for i in os.listdir(my_dir):
        with open(my_dir + i, encoding="utf8") as json_file:
            data = json.load(json_file)
            for key in data:
                if (id == key['id']):
                    return key['text'] 
            print("No existing tweet")