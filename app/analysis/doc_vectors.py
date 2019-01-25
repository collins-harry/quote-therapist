from quote_mappers import quote_mapper
import numpy as np

def return_special_vectors():

    quoteVectorPairs = []

    vectors = quote_mapper.getDocvectors(None, None)

    origin_vector = np.zeros(100)
    origin_vector -= .34

    home = quote_mapper.find_closest_vectors(origin_vector, vectors)[0]
    quote = home[0]
    dist = home[1]
    vector = home[2]

    quoteVectorPairs.append((home[0], home[2]))

    home2 = quote_mapper.find_closest_vectors(vector, vectors, flag=True)[1]

    quoteVectorPairs.append((home2[0], home2[2]))

    home3 = quote_mapper.find_closest_vectors(home2[2], vectors, num_vectors=-1)[-10]

    quoteVectorPairs.append((home3[0], home3[2]))

    return quoteVectorPairs


if __name__ == '__main__':
    return_special_vectors()
