'''
K-MEANS
=======
(for faster you can use precompute_distances (uses more memory))

attributes
==========
inertia_ : sum squared distances to cluster centre

transform(X)

model.cluster_centers_ (shape - n_clusters, n_features)
'''
from sklearn.cluster import KMeans
import numpy as np
from quote_mappers.quote_mapper import getDocvectors
import matplotlib.pyplot as plt
import os
import pickle
import csv
from sklearn.decomposition import PCA




def main():
    model, labels = get_model(n_clusters = 10, new_model=True, return_labels=True)    
    create_reduced_cluster_csv(model, 2)

    # print(labels)
    # create_cluster_csv(model)


def create_reduced_cluster_csv(model, n_dimension, name='redu_cluster.csv'):
    clusters = model.cluster_centers_
    reduced_clusters = get_reduced_vectors(clusters, n_dimension=n_dimension)
    with open(name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(reduced_clusters)
    print('clusters written to clusters.csv')
     

def get_reduced_vectors(vectors, n_dimension=3):
    pca_model = PCA(n_components=n_dimension)
    reduced_vectors = pca_model.fit_transform(vectors)
    return reduced_vectors
    

def import_docvectors():
    try:
        docvectors = getDocvectors(None, None)
        return docvectors
    except:
        raise ValueError('getDocvectors cannot find or import the presaved models')


def plot_cluster_sizes(cluster_num, name='foo.png'):
    '''
    runs and plots K-means from 1 until cluster_num
    '''
    quotesvector = import_docvectors()
    #quotesvector organised as list of ['quote', array([ docvector]) ]
    raw_vectors = np.array([quotesvector[x][1] for x in range(len(quotesvector))])

    inertias = []
    for i in range(1,cluster_num+1):
        inertias.append(1000000)
        print(f'finished cluster = {i}')
        for j in range(1,5):
            model = KMeans(n_clusters=i)
            labels = model.fit_predict(raw_vectors) #shape = n_samples, n_features
            inertia = model.inertia_
            if inertia < inertias[-1]:
                inertias[i-1] = inertia

    x = list(range(1, len(inertias)+1))
    plot = plt.plot(x, inertias)
    plt.savefig(os.getcwd() + '/plots/foo.png')
    print(f'plot saved to {os.getcwd()}' + f"/plots/{name}")


def get_model(name='kmeans', n_clusters=50, new_model=False, return_labels=False):
    '''
    Imports trained model along with cluster info.
    If trained model not available it will create a new model
    '''

    filename = str(n_clusters) + '_cluster_kmeans.p'
    path = os.getcwd() + '/models/' + filename

    if os.path.isfile(path) and not new_model:
        'using pretrained model'
        with open(path, "rb") as f:
            model, labels = pickle.load(f)

        if return_labels:
            return model, labels
        else:
            return model

    else:
        doc_vectors = import_docvectors()
        raw_vectors = np.array([doc_vectors[x][1] for x in range(len(doc_vectors))])
        model = KMeans(n_clusters=n_clusters)
        inertia = 1000000
        for i in range(5):
            labels = model.fit_predict(raw_vectors)
            if model.inertia_ < inertia:
                best_model = model
                best_model_labels = labels
                inertia = model.inertia_

        with open(path, "wb") as f:
            pickle.dump((best_model, best_model_labels), f)

        if return_labels:
            return best_model, best_model_labels
        else:
            return best_model

def create_cluster_csv(model, name='clusters.csv'):
    clusters = model.cluster_centers_
    with open(name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(clusters)
        print('clusters written to clusters.csv')


if __name__ == '__main__':
    main()
