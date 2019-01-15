from gensim.models import Doc2Vec, Word2Vec
from gensim.models.doc2vec import TaggedDocument
import json
import numpy as np
from time import sleep
from string import punctuation
from qoute_functions.get_keywords import get_keywords
from nltk.corpus import stopwords
import nltk
from collections import defaultdict
import pickle
import os
import random
from datetime import datetime
nltk.download('stopwords')

script_dir = os.path.dirname(os.path.realpath(__file__))
current_dir = os.getcwd()
stopwords = set(stopwords.words('english'))

dimensions = 100
full_dataset = False

def getDictionary(quotes):
    path = current_dir + "dictionary/freq_dic.p"
    if os.path.exists(path):
        with open(path, 'rb') as f:
            freq_dic = pickle.load(f)
    else:
        freq_dic = defaultdict(int)
        for quote in quotes:
            for word in quote.split():
                word = word.lower()
                freq_dic[word] += 1

        with open(path, 'wb') as f:
            pickle.dump(freq_dic, f)

    return freq_dic


def loadGlove(filename=current_dir + "/glove/glove.6B.100d.txt"):
    f = open(filename, 'r', encoding='utf-8')
    model = {}
    counter = 0
    for line in f:
        counter += 1
        if counter % 100000 == 0:
            print("Reading line", counter)
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding

    print("Finished loading model!")
    return model

def loadQuotes(filename):
    with open(filename, 'r') as f:
        poems = json.load(f)
        return poems

def getWordVector(word, model):
    word = ''.join(c for c in word.lower() if c not in punctuation)
    try:
        vector = model[word]
        return vector
    except:
        return []

def getWordVectors(quote, model):
    vectors = []
    keywords = [x for x in quote.split() if x not in stopwords]
    for word in keywords:
        vector = getWordVector(word.lower(), model)
        if len(vector) > 1:
            vectors.append(vector)

    return vectors

def getDistance(input, quote, model, freq_dic):
    distance = 0
    input = input.split()
    quote = quote.split()

    for word_in in input:
        distances = []
        for word_quote in quote:
            try:
                dist = np.linalg.norm(np.array(getWordVector(word_in, model)) - np.array(getWordVector(word_quote, model)))
                if freq_dic[word_in.lower()] != 0:
                    dist += 0.02 * np.log(freq_dic[word_in.lower()] * freq_dic[word_quote.lower()])
                else:
                    dist += 0.02 * np.log(freq_dic[word_quote.lower()])
            except:
                continue
            distances.append(dist)

        try:
            distance += min(distances)
        except:
            continue

    distance += 0.6 * len(quote)
    return distance

def filterKeywords(quote):
    words = ' '.join([x for x in get_keywords(quote, ["NOUN", "ADJ", "ADV"])])
    return words

def getQuoteForInput(input, model):
    quotes = loadQuotes(current_dir + "/qoutes/wiseoldsayings.json")
    input = filterKeywords(input)
    if full_dataset:
        quotes.extend(loadQuotes(current_dir + "/qoutes/quoteland.json"))

    freq_dic = getDictionary(quotes)
    best_vectors = []
    for quote in quotes:
        quote = quote["poem"]
        dist = getDistance(input, quote, model, freq_dic)
        best_vectors.append([quote, dist])

    best_vectors.sort(key=lambda x: x[1])
    for quote in [x[0] for x in best_vectors]:
        if len(quote.split()) > 4:
            return quote


