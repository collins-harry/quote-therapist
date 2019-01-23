'''
K-MEANS
=======
(for faster you can use precompute_distances (uses more memory))

attributes
==========
inertia_ : sum squared distances to cluster centre

transform(X)


'''
from sklearn.cluster import KMeans
import numpy as np
from quote_mappers.quote_mapper import getDocvectors
import matplotlib.pyplot as plt

def import_vectors():
    try:
        vectors = getDocvectors(None, None)
        return vectors
    except:
        raise ValueError('getDocvectors cannot find or import the presaved models')
 
qoutesvector = import_vectors()
#qoutesvector organised as list of ['qoute', array([ docvector]) ]
vectors = np.array([qoutesvector[x][1] for x in range(len(qoutesvector))])


inertias = []
for i in range(1,101):
    inertias.append(1000000)
    print(f'finished cluster = {i}')
    for j in range(1,5):
        model = KMeans(n_clusters=i)
        labels = model.fit_predict(vectors) #shape = n_samples, n_features
        inertia = model.inertia_
        if inertia < inertias[-1]:
            inertias[i-1] = inertia

x = list(range(1, len(inertias)+1))
plot = plt.plot(x, inertias)
plt.savefig('foo.png')

