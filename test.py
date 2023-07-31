import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, MeanShift, AffinityPropagation, Birch, MiniBatchKMeans
from sklearn.metrics import silhouette_score
import pandas as pd

class ClusteringEvaluator:
    def __init__(self, data, max_clusters):
        self.data = data
        self.max_clusters = max_clusters
        self.algorithms = {
            "K-Means": KMeans,
            "Agglomerative Clustering": AgglomerativeClustering,
            "DBSCAN": DBSCAN,
            "Mean Shift": MeanShift,
            "Affinity Propagation": AffinityPropagation,
            "BIRCH": Birch,
            "Mini-Batch K-Means": MiniBatchKMeans
        }

    def _calculate_silhouette_score(self, algorithm, num_clusters):
        algo_class = self.algorithms[algorithm]
        if algorithm == "DBSCAN":
            algo = algo_class(eps=0.5, min_samples=num_clusters)
        else:
            algo = algo_class(n_clusters=num_clusters)
        cluster_labels = algo.fit_predict(self.data)
        score = silhouette_score(self.data, cluster_labels)
        return score

    def find_best_clusters(self):
        best_clusters_dict = {}

        for algo_name, algo_class in self.algorithms.items():
            best_clusters = 2  # Default value
            best_score = -1

            for n_clusters in range(2, self.max_clusters + 1):
                score = self._calculate_silhouette_score(algo_name, n_clusters)

                if score > best_score:
                    best_clusters = n_clusters
                    best_score = score

            best_clusters_dict[algo_name] = best_clusters

        return best_clusters_dict

    def plot_elbow_method(self, algorithm, max_clusters=None):
        if max_clusters is None:
            max_clusters = self.max_clusters

        distortions = []
        for n_clusters in range(1, max_clusters + 1):
            if algorithm == "DBSCAN":
                continue
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(self.data)
            distortions.append(kmeans.inertia_)

        plt.plot(range(1, max_clusters + 1), distortions, marker='o')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Distortion (Inertia)')
        plt.title(f'Elbow Method for {algorithm}')
        plt.show()

    def evaluate_best_algorithm(self, best_clusters):
        evaluation_results = {}

        for algo_name, num_clusters in best_clusters.items():
            algo_class = self.algorithms[algo_name]
            if algo_name == "DBSCAN":
                algo = algo_class(eps=0.5, min_samples=num_clusters)
            else:
                algo = algo_class(n_clusters=num_clusters)
            cluster_labels = algo.fit_predict(self.data)
            score = silhouette_score(self.data, cluster_labels)
            evaluation_results[algo_name] = score

        return evaluation_results


# Example usage:
if __name__ == "__main__":
    # Assuming you have the 'data' array containing the data points for clustering
    data = pd.read_csv(r'C:\Python_project\Customer-Personality-Analysis\artifact\pcadata.csv')

    max_clusters = 10  # You can set the maximum number of clusters you want to consider
    clustering_evaluator = ClusteringEvaluator(data, max_clusters)

    best_clusters = clustering_evaluator.find_best_clusters()
    print("Best Number of Clusters for Each Algorithm:", best_clusters)

    # To perform the Elbow Method for K-Means with a specific algorithm:
    # clustering_evaluator.plot_elbow_method("K-Means", max_clusters=10)

    evaluation_results = clustering_evaluator.evaluate_best_algorithm(best_clusters)
    print("Evaluation Results:", evaluation_results)
