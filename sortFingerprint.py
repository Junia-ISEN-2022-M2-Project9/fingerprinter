#import xlsxwriter
from difflib import SequenceMatcher
import sys
import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering

def main(aFile):
    return sortFile(aFile)


####
# Take a file as input and give an xlsx as output. This xlsx gives all the distances between the fingerprints. The current distance used is the hamming distance for
# now. 
####

def sortFile(fileLocation):
    listOfFingerprints=[]
    file = open(fileLocation, "r")
    for line in file:
        listOfFingerprints.append(line.replace('\n','')) #retire le retour a la ligne a la fin des fingerprints
    listOfFingerprints=list(set(listOfFingerprints)) # retire les doublons

    #print(listOfFingerprints)

    listDistances=[] # list of list (matrix). Chaque liste contient l'ensemble des distances par rapport a une empreinte. 
    for fingerprint in listOfFingerprints:
        listOfDist=[]
        for fingerprint2 in listOfFingerprints: 
            listOfDist.append(distance(fingerprint,fingerprint2))
        listDistances.append(listOfDist)
    print(listDistances)

def distance(f1,f2):
    return(1-SequenceMatcher(None,f1,f2).ratio())


# Hierarchical clustering


def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

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


iris = load_iris()
X = iris.data

# setting distance_threshold=0 ensures we compute the full tree.
model = AgglomerativeClustering(distance_threshold=0, n_clusters=None)

model = model.fit(X)
plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
plot_dendrogram(model, truncate_mode="level", p=3)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()





































########################### OLD ##########################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################
##########################################################################################################################################


"""
    listOfFingerprints = ["liste contenant toutes fingerprints differentes"]
    listOfSplitedFingerprints=[]
    numberOfsameFingerprint = ["nombre de fringerprint semblable a celle du meme indice dans liste precedente"]
    file = open(fileLocation, "r")
    for line in file:
        testMatch = False
        k=len(listOfFingerprints)
        for i in range(0, k):
            if hamming_distance(listOfFingerprints[i], line) == 0:
                numberOfsameFingerprint[i] += 1
                testMatch = True
            if i == len(listOfFingerprints)-1 and not testMatch:
                listOfFingerprints.append(line)
                numberOfsameFingerprint.append(1)
    listOfFingerprints.pop(0)
    numberOfsameFingerprint.pop(0)
    print("This is the list of the figerprints found\n")
    print(listOfFingerprints)
    print("\nHow many of them in the file:\n")
    print(numberOfsameFingerprint)
    for x in listOfFingerprints:
        listOfSplitedFingerprints.append(x.split('|'))
    listOfDistances=calculateDistanceBetweenFingerprints(listOfSplitedFingerprints)
    print(max(listOfDistances))
    file.close()
"""


"""
###
# Calculate the distances between all the fingerprints given in a list, as a list of subcategories.
###

def calculateDistanceBetweenFingerprints(aListOfSplitedFingerprints):
    listOfDistances=[]
    indice=0
    while len(aListOfSplitedFingerprints)!=1:
        listOfDistances.append([])
        fingerprintToCompare= aListOfSplitedFingerprints.pop(0)
        for i in range(0,len(aListOfSplitedFingerprints)):
            listOfDistances[indice].append(sumSubcategoriesDistances(fingerprintToCompare,aListOfSplitedFingerprints[i]))
        indice+=1
    return(listOfDistances)
"""
"""
###   
# calculate the complete distance between two fingerprints. 
###

def sumSubcategoriesDistances(firstFingerprint, secondFingerprint):
    totalDistance=0
    for i in range (len(firstFingerprint)):
        totalDistance+=hamming_distance(firstFingerprint[i],secondFingerprint[i])
    return(totalDistance)
"""
###
# Write in an xlsx file the distances associated to a list of Fringerprints. 
###
"""
def writeInXlsx(aListofDistance,aListOfFingerprints):
    workbook = xlsxwriter.Workbook('hello.xlsx')
    worksheet = workbook.add_worksheet()
    for k in range (len(aListOfFingerprints)):
        if k<=24:
            x=chr(66+k)+'1'
        if k==25:
            x='AA1'
        if k>25:
            x=chr(64+k//26)+chr(65+(k%26))+'1'
        y='A'+str(k+2)
        worksheet.write(x,str(aListOfFingerprints[k]))
        worksheet.write(y,str(aListOfFingerprints[k]))
    for z in range (len(aListofDistance)):
        for y in range (len(aListofDistance[z])):
            if y<=23-z:
                x=chr(67+y+z)+str(2+z)
            if y==24-z:
                x='AA'+str(2+z)
            if y>24-z:
                x=chr(64+(y+1+z)//26)+chr(65+((y+1+z)%26))+str(2+z)
            worksheet.write(x,str(aListofDistance[z][y]))
    workbook.close()
"""


"""
###
# determine the hamming_distance between two fingerprints. 
###

# Distance de levenstein 
def hamming_distance(string1, string2):
    shortestLength = min(len(string1),len(string2))
    dist_counter = abs(len(string1)-len(string2))
    for n in range(shortestLength):
        if string1[n] != string2[n]:
            dist_counter += 1
    return dist_counter

if len(sys.argv)!=2:
    print("an argument with the list of the firgerprints must be given")
    exit(1)
"""

