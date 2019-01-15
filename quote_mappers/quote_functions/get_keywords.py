import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')

#string = sys.argv[1]
#print(f'word, tags (treebank): {wordtags_treebank}')
#print(f'word, tags (universal): {wordtags_universal}')
#wordtags_treebank = nltk.pos_tag(words)

def get_keywords(text, keyword_tags = ['NOUN'], wordnet = False, stop_words = False):
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
    if wordnet:
        keywords = [(word, tag) for word, tag in tagged_words if tag in keyword_tags]
    else:
        keywords = [word for word, tag in tagged_words if tag in keyword_tags]

    return keywords

if __name__ == '__main__':
    print(get_keywords('I love to eat jumbo prawns', keyword_tags = ['NOUN', 'VERB'], stop_words = True))

