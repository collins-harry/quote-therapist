from gensim.models import Doc2Vec, Word2Vec
from gensim.models.doc2vec import TaggedDocument
import json
import numpy as np
from time import sleep
from string import punctuation
from qoute_functions.get_keywords import get_keywords
from nltk.corpus import stopwords
import nltk
import pickle
import os
import random
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))

dimensions = 100
full_dataset = False

def loadGlove(filename = "glove/glove.6B.100d.txt"):
    f = open(filename, 'r')
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
        return None

def trainDoc2Vec(quotes):
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(quotes)]
    model = Doc2Vec(documents, vector_size=5, window=2, min_count=1, workers=4)
    return model

def getDocVector(quote, model):
    vectors = []
    for word in get_keywords(quote, ["NOUN", "ADJ", "ADV", "VERB"]):
        if word not in stopwords:
            word = ''.join(c for c in word.lower() if c not in punctuation)
            try:
                vectors.append(model[word])
            except:
                continue

    return np.average(vectors, axis=0)

def getDocvectors(quotes, model):
    #path = "models/docvectors.p"
    if full_dataset:
        path = "models/" + str(dimensions) + "_docvectors_large.p"
    else:
        path = "models/" + str(dimensions) + "_docvectors.p"

    if os.path.isfile(path):
        with open(path, "rb") as f:
            vectors = pickle.load(f)
            return vectors
    else:
        vectors = []
        i = 0
        for quote in quotes:
            i += 1
            if i % 100 == 0:
                print("Mapping quote", i)
            quote = quote["poem"]
            docvector = getDocVector(quote, model)
            vectors.append([quote, docvector])

        with open(path, "wb") as f:
            pickle.dump(vectors, f)

        return vectors

def getQuoteForInput(input, model):
    quotes = loadQuotes("qoutes/wiseoldsayings.json")
    if full_dataset:
        quotes.extend(loadQuotes("qoutes/quoteland.json"))

    vectors = getDocvectors(quotes, model)

    sentence_vector = getDocVector(input, model)

    best_vectors = []
    for quote, vector in vectors:
        dist = np.linalg.norm(np.array(vector) - np.array(sentence_vector))
        dist += 0.005 * len(quote)
        best_vectors.append([quote, dist])

    best_vectors.sort(key=lambda x: x[1])
    return [x[0] for x in best_vectors[:4]]

