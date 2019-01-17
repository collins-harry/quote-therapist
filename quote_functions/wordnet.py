import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from itertools import product

def test():
    lst = [('boat','NOUN'),
            ('car','NOUN'),
            ('ship','NOUN'),
            ('animal','NOUN'),
            ('monkey','NOUN'),
            ('banana','NOUN'),
            ('run', 'VERB'),
            ('attacking', 'VERB')]
    lst2 = [create_synset(word, tag) for word, tag in lst]

    for w1, w2 in product(lst2, lst2):
        print(f'{w1}, {w2}: {compare_similiarity(w1, w2)}')


def create_synset(word, tag):
    if tag == 'NOUN':
        tag = 'n'
    elif tag == 'VERB':
        tag = 'v'
    elif tag == 'ADV':
        tag = 'r'
    elif tag == 'ADJ':
        tag = 'a'
    #try:
    #    return wn.synset(f'{word}.{tag}.01')
    #except:
    #    try:
    #        word = WordNetLemmatizer().lemmatize(word, pos=tag)
    #        return wn.synset(f'{word}.{tag}.01')
    #    except:
    #        return None
    try:
        word = WordNetLemmatizer().lemmatize(word, pos=tag)
        return wn.synset(f'{word}.{tag}.01')
    except:
        return None


def compare_similiarity(synset1, synset2, measure = 'wup'):
    if measure == 'wup':
        simil = synset1.wup_similarity(synset2)
        if simil == None:
            simil = 0
        return simil

if __name__ == '__main__':
    test()

