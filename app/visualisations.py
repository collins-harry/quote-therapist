import analysis.k_means as k_means
import matplotlib.pyplot as plt
import os
import numpy as np
import analysis.doc_vectors

def plot_clusters(n_clusters=50, n_dimensions=2):
    model = k_means.get_model(n_clusters=n_clusters)
    clusters = model.cluster_centers_
    reduced_clusters = k_means.get_reduced_vectors(clusters, n_dimension=n_dimensions)
    x = reduced_clusters[:,0]
    y = reduced_clusters[:,1]

    plt.scatter(x, y)
    plt.savefig(os.getcwd() + f'/plots/{n_dimensions}dim{n_clusters}clusters.png')

    print(f'plotted into /plots/{n_dimensions}dim{n_clusters}clusters.png')


def plot_quotes(n_dimensions=2, flagged_vectors=None):
    doc_vectors = k_means.import_docvectors()
    raw_vectors = np.array([doc_vectors[x][1] for x in range(len(doc_vectors))])
    reduced_vectors, pca_model = k_means.get_reduced_vectors(raw_vectors, n_dimensions=n_dimensions, return_model=True)
    x = reduced_vectors[:,0]
    y = reduced_vectors[:,1]
    plt.scatter(x, y)
    if flagged_vectors != None:
        flagged_vectors = pca_model.transform(flagged_vectors)
        # print(flagged_vectors)
        x = np.array(flagged_vectors)[:,0]
        y = np.array(flagged_vectors)[:,1]
        plt.scatter(x,y)
    plt.savefig(os.getcwd() + f'/plots/{n_dimensions}dim_allquotes.png')
    print(f'plotted into /plots/{n_dimensions}dim_allquotes.png')


if __name__ == '__main__':
    special_vectors = analysis.doc_vectors.return_special_vectors()
    flagged_vectors = [vector[1] for vector in special_vectors]
    plot_quotes(flagged_vectors=flagged_vectors)
    print('QOUTES', '\n------------')
    for vector in special_vectors:
        print(vector[0])

    # plot_clusters(n_clusters=50, n_dimension=2)





#### OTHER ####
# doc_vectors = k_means.import_docvectors()
# raw_vectors = np.array([doc_vectors[x][1] for x in range(len(doc_vectors))])
# reduced_vectors = k_means.get_reduced_vectors(raw_vectors, n_dimensions=2)
# pot_vectors = [(index, vector) for index, vector in enumerate(reduced_vectors) if 1.9 < vector[0] < 1.95][-1]
#print(doc_vectors[pot_vectors][0]])

# last_vector = [(index, vector) for index, vector in enumerate(reduced_vectors) if 1.9 < vector[0] < 1.95][-1]
# print(last_vector)
# flagged_vectors.append(doc_vectors[last_vector[0]][1])
# flagged_vectors = k_means.get_reduced_vectors(flagged_vectors, n_dimensions=n_dimensions)
# print(flagged_vectors)


