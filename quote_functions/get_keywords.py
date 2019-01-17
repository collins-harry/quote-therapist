import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
# from wordnet import create_synset, compare_similiarity
from nltk.corpus import wordnet
import random as rand 

nltk.download("punkt")
nltk.download("wordnet")
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

#string = sys.argv[1]
#print(f'word, tags (treebank): {wordtags_treebank}')
#print(f'word, tags (universal): {wordtags_universal}')
#wordtags_treebank = nltk.pos_tag(words)

def get_keywords(text, keyword_tags = ['NOUN'], word_net = False, stop_words = False):
    """returns: an array of all words with specified pos_tags 
    params: 
        text -- string 
        keyword_tags -- defaults to ['NOUN'], other options include ['NOUN', 'VERB'] etc. uses universal tagset.
    """
    words = nltk.word_tokenize(text)
    tagged_words = nltk.pos_tag(words, tagset='universal')
    
    # using stopwords method of getting keywords
    if stop_words == True:
        stopword_set = set(stopwords.words('english'))
        keywords = [x for x in text.lower().split() if x not in stopword_set]
        return keywords

    # different requirements if using wordnet similiarity model vs word vector.
    if word_net:
        keywords = [(word.lower(), tag) for word, tag in tagged_words if tag in keyword_tags]
    else:
        keywords = [word.lower() for word, tag in tagged_words if tag in keyword_tags]

    return keywords

def get_synonyms(text, keyword_tags = ['NOUN'], word_net = True):
    keywords = get_keywords(text, keyword_tags=keyword_tags, )
    print(keywords)
    synsets = [wordnet.synsets(keyword) for keyword in keywords]
    print(synsets)
    keyword_synonyms = []
    for syn in synsets:
        rand.shuffle(syn)
        keyword_synonyms.append(syn[0].lemmas()[0].name())
    print(keyword_synonyms)
    return keyword_synonyms
    

if __name__ == '__main__':
    print(get_keywords('Acting deals with very delicate emotions. It is not putting up a mask. Each time an actor acts he does not hide; he exposes himself', 
                        keyword_tags = ['NOUN'],
                        ))
    get_synonyms('Acting deals with very delicate emotions. It is not putting up a mask. Each time an actor acts he does not hide; he exposes himself', keyword_tags = ['NOUN'])

