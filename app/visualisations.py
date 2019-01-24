import analysis.k_means as k_means
import matplotlib.pyplot as plt
import os


def plot_clusters(n_clusters=50, n_dimension=2):
    model = k_means.get_model(n_clusters=n_clusters)
    clusters = model.cluster_centers_
    reduced_clusters = k_means.get_reduced_vectors(clusters, n_dimension=n_dimension)
    x = reduced_clusters[:,0]
    y = reduced_clusters[:,1]

    plt.scatter(x, y)
    plt.savefig(os.getcwd() + f'/plots/{n_dimension}dim{n_clusters}clusters.png')

    print(f'plotted into /plots/{n_dimension}dim{n_clusters}clusters.png')

plot_clusters(n_clusters=50, n_dimension=2)
