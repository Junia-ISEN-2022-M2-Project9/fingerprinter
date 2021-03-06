#!/bin/python
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from difflib import SequenceMatcher
import jellyfish


# -----------------------FONCTIONS------------------------#


# Fonction de calcul de distance avec sequenceMatcher

def distance(f1, f2):
    return (1 - SequenceMatcher(None, f1,
                                f2).ratio())  # isjunk=None (no element ignored), .ratio give float between [0,1]


# Fonction de calcul de distance avec jellyfish
# Uncomment to use levenstein distance
"""
def distance(f1,f2):
    return(jellyfish.levenshtein_distance(f1,f2))
"""
# Uncomment to use jaro distance
"""
def distance(f1,f2):
    return(jellyfish.jaro_distance(f1,f2))
"""
# Uncomment to use damerau levenstein distance
"""
def distance(f1,f2):
    return(jellyfish.damerau_levenshtein_distance(f1,f2))
"""


# Fonction d'affichage du dendogramme
def plot_dendrogram(model, **kwargs):
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
                counts[i] = current_count

                linkage_matrix = np.column_stack(
                    [model.children_, model.distances_, counts]
                ).astype(float)

                # Plot the corresponding dendrogram
                dendrogram(linkage_matrix, **kwargs)


# --------------------------MAIN--------------------------#

def main():
    # Formatage des empreintes
    listOfFingerprints = []
    listWithAllTaggedFingerprints = []
    for z in range(len(sys.argv) - 1):
        filePath = sys.argv[z + 1]
        with open(filePath, "r") as file:
            listOfFingerprintsInFile = [line.replace('\n', '') for line in file]
            # listOfFingerprints.append(line.replace('\n','')) #retire le retour a la ligne a la fin des fingerprints
            listOfFingerprintsInFile = list(set(listOfFingerprintsInFile))  # retire les doublons
            listOfFingerprintsInFile2 = []
            for y in range(len(listOfFingerprintsInFile)):
                listOfFingerprintsInFile2.append([listOfFingerprintsInFile[y], filePath])
        listOfFingerprints.extend(listOfFingerprintsInFile)
        listWithAllTaggedFingerprints.extend(listOfFingerprintsInFile2)

    # Cr??ation de la matrice de distances
    listDistances = []  # Chaque liste contient l'ensemble des distances par rapport a une empreinte.
    for fingerprint in listOfFingerprints:
        listOfDist = []
        for fingerprint2 in listOfFingerprints:
            listOfDist.append(distance(fingerprint, fingerprint2))
        listDistances.append(listOfDist)

    # Cr??ation du mod??le
    model = AgglomerativeClustering(distance_threshold=None,
                                    n_clusters=2)  # n_cluster= number of cluster to find, if not none distance must be none.
    model = model.fit(listDistances)

    # Affichage
    plt.title("Dendogramme de Regroupement Hierarchique")
    # plot_dendrogram(model, truncate_mode="level", p=10) # plot the top ten levels of the dendrogram
    plt.xlabel("Nombre de points dans un noeud (ou index de point s'il n'y a pas de parenth??se)")
    plt.ylabel("Distance entre les clusters")
    # plt.show()
    # print(model.n_clusters_)
    # print(model.labels_)

    for k in range(model.n_clusters_):
        # Will be reset for each cluster needed
        stats = {}  # dictionary containing stats for a cluster
        results = []  # contains wanted fingerprints followed by its txt source
        print("\ncluster number " + str(k))
        for p in range(len(listOfFingerprints)):
            if model.labels_[p] == k:
                results.append(listOfFingerprints[p] + ' ' + listWithAllTaggedFingerprints[p][1])
        # show some stats
        # fetch name at each end of fingerprint and count in a dictionary
        for finger in results:
            # split with space presence
            text_file_name = re.split("\s", finger)
            # dict exists
            if text_file_name[1] in stats:
                stats[text_file_name[1]] += 1
            # dict does not exist
            else:
                stats[text_file_name[1]] = 1
        # do maths with stats dictionary
        cluster_size = 0
        for key in stats:
            cluster_size += stats[key]
        for key in stats:
            stats[key] = str(round(stats[key]/cluster_size*100, 2)) + "%"
        print(stats)
        for res in results:
            print(res)


if __name__ == '__main__':
    main()

# Formatage des empreintes
listOfFingerprints = []
listWithAllTaggedFingerprints = []
for z in range(len(sys.argv) - 1):
    filePath = sys.argv[z + 1]
    with open(filePath, "r") as file:
        listOfFingerprintsInFile = [line.replace('\n', '') for line in file]
        # listOfFingerprints.append(line.replace('\n','')) #retire le retour a la ligne a la fin des fingerprints
        listOfFingerprintsInFile = list(set(listOfFingerprintsInFile))  # retire les doublons
        listOfFingerprintsInFile2 = []
        for y in range(len(listOfFingerprintsInFile)):
            listOfFingerprintsInFile2.append([listOfFingerprintsInFile[y], filePath])
    listOfFingerprints.extend(listOfFingerprintsInFile)
    listWithAllTaggedFingerprints.extend(listOfFingerprintsInFile2)

# Cr??ation de la matrice de distances
listDistances = []  # Chaque liste contient l'ensemble des distances par rapport a une empreinte.
for fingerprint in listOfFingerprints:
    listOfDist = []
    for fingerprint2 in listOfFingerprints:
        listOfDist.append(distance(fingerprint, fingerprint2))
    listDistances.append(listOfDist)

# Cr??ation du mod??le
model = AgglomerativeClustering(distance_threshold=None,
                                n_clusters=3)  # n_cluster= number of cluster to find, if not none distance must be none.
model = model.fit(listDistances)

# Affichage
plt.title("Dendogramme de Regroupement Hierarchique")
# plot_dendrogram(model, truncate_mode="level", p=10) # plot the top ten levels of the dendrogram
plt.xlabel("Nombre de points dans un noeud (ou index de point s'il n'y a pas de parenth??se)")
plt.ylabel("Distance entre les clusters")
# plt.show()
# print(model.n_clusters_)
# print(model.labels_)
for k in range(model.n_clusters_):
    print("\ncluster number " + str(k))
    for p in range(len(listOfFingerprints)):
        if model.labels_[p] == k:
            print(listOfFingerprints[p] + ' ' + listWithAllTaggedFingerprints[p][1])
