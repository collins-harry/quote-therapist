from gensim.models import Doc2Vec, Word2Vec
from gensim.models.doc2vec import TaggedDocument
import json
import numpy as np
from time import sleep
from string import punctuation
from qoute_functions.get_keywords import get_keywords
from nltk.corpus import stopwords
from quote_functions.wordnet import create_synset, compare_similiarity
import nltk
import pickle
import os
import random
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))

dimensions = 100
full_dataset = False

def loadQuotes(filename):
    with open(filename, 'r') as f:
        poems = json.load(f)
        return poems

def getSysnets(quote):
    keyword_tag_pair = get_keywords(quote, keyword_tags=["NOUN", "ADJ", "ADV", "VERB"], wordnet=True)
    quote_sysnets = []
    for word, tag in keyword_tag_pair:
        sysnet = create_synset(word.lower(), tag)
        quote_sysnets.append(sysnet)
    return quote_sysnets

def getSimiliarity(input, quote):
    similiarity = 0
    input_sysnets = getSysnets(input)
    quote_sysnets = getSysnets(quote)

    input_length = len(input_sysnets)
    for input_sysnet in input_sysnets:
        similiarities = []
        for quote_sysnet in quote_sysnets:
            try:
                simil = compare_similiarity(input_sysnet, quote_sysnet)
            except:
                simil = 0
            similiarities.append(simil)
        try:
            similiarity += max(similiarities)
        except:
            continue

    similiarity /= input_length
    return similiarity


def getQuoteForInput(input):
    quotes = loadQuotes("qoutes/wiseoldsayings.json")
    if full_dataset:
        quotes.extend(loadQuotes("qoutes/quoteland.json"))

    best_vectors = []
    for index, quote in enumerate(quotes):
        if index%100 ==0:
            print(f'qoutes_processed: {index}')
        quote = quote["poem"]
        simil = getSimiliarity(input, quote)
        best_vectors.append([quote, simil])

    best_vectors.sort(key=lambda x: x[1])
    return best_vectors[-1][0]


quote = "I am going to the grocery store"
print(getQuoteForInput(quote))

