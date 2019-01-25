import json
import numpy as np
from time import sleep
from string import punctuation
from quote_functions.get_keywords import get_keywords
from nltk.corpus import stopwords
import nltk
import pickle
import os
import random
nltk.download('stopwords')

stopwords = set(stopwords.words('english'))

dimensions = 100
full_dataset = False
current_dir = os.getcwd()

def main():
    input_quote = input('quote: ')
    output_quote = getQuote(input_quote, loadGlove())
    print(output_quote)

def loadGlove(filename = "/glove/glove.6B.100d.txt"):
    f = list(open('glove/glove_100d_1.txt', 'r', encoding="utf8"))
    f += list(open('glove/glove_100d_2.txt', 'r', encoding="utf8"))
    f += list(open('glove/glove_100d_3.txt', 'r', encoding="utf8"))
    f += list(open('glove/glove_100d_4.txt', 'r', encoding="utf8"))
    
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
        path = "models/docvectors_large.p"
    else:
        path = "models/docvectors.p"

    if os.path.isfile(path):
        print('found pretrained docvectors')
        with open(path, "rb") as f:
            vectors = pickle.load(f)
            return vectors
    else:
        print('creating docvectors manually')
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

def getQuote(input, model):
    quotes = loadQuotes(current_dir + "/quotes/wiseoldsayings.json")
    if full_dataset:
        quotes.extend(loadQuotes(current_dir + "/quotes/quoteland.json"))

    vectors = getDocvectors(quotes, model)

    sentence_vector = getDocVector(input, model)

    closest_vectors = find_closest_vectors(sentence_vector, vectors)

    quotes = [x[0] for x in closest_vectors]
    return random.sample(quotes, 1)[0]


def find_closest_vectors(sentence_vector, vectors, num_vectors=1, flag=False):
    '''
    returns closest vectors shape() = [qoute, dist, vector]
    '''
    if flag:
        num_vectors += 1

    best_vectors = []
    for quote, vector in vectors:
        dist = np.linalg.norm(np.array(vector) - np.array(sentence_vector))
        dist += 0.005 * len(quote)
        best_vectors.append([quote, dist, vector])

    best_vectors.sort(key=lambda x: x[1])
    return best_vectors[:num_vectors]




if __name__ == '__main__':
    main()
