#!/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering
from difflib import SequenceMatcher

#-----------------------FONCTIONS------------------------#


# Fonction de calcul de distance
def distance(f1,f2):
    return(1-SequenceMatcher(None,f1,f2).ratio())

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


#--------------------------MAIN--------------------------#

def main():
    # Formatage des empreintes
    filePath = sys.argv[1]
    with open(filePath, "r") as file:
        listOfFingerprints = [line.replace('\n', '') for line in file]
        #listOfFingerprints.append(line.replace('\n','')) #retire le retour a la ligne a la fin des fingerprints
        listOfFingerprints=list(set(listOfFingerprints)) # retire les doublons


    # Création de la matrice de distances
    listDistances=[] # Chaque liste contient l'ensemble des distances par rapport a une empreinte.
    for fingerprint in listOfFingerprints:
        listOfDist=[]
        for fingerprint2 in listOfFingerprints:
            listOfDist.append(distance(fingerprint,fingerprint2))                    
        listDistances.append(listOfDist)


    # Création du modèle
    model = AgglomerativeClustering(distance_threshold=0, n_clusters=None) # setting distance_threshold=0 ensures we compute the full tree
    model = model.fit(listDistances)


    # Affichage
    plt.title("Dendogramme de Regroupement Hierarchique")
    plot_dendrogram(model, truncate_mode="level", p=3) # plot the top three levels of the dendrogram
    plt.xlabel("Nombre de points dans un noeud (ou index de point s'il n'y a pas de parenthèse)")
    plt.ylabel("Distance entre les clusters")
    plt.show()
    

if __name__ ==  '__main__':
    main()
