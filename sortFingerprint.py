import time


def sortFile(fileLocation):
    listOfFingerprints = ["liste contenant toutes fingerprints differentes"]
    listOfSplitedFingerprints=[]
    numberOfsameFingerprint = ["nombre de fringerprint semblable a celle du même indice dans liste precedente"]
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
    for x in listOfFingerprints:
        listOfSplitedFingerprints.append(x.split('|'))
    print(calculateDistanceBetweenFingerprints(listOfSplitedFingerprints))
    file.close()

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

def sumSubcategoriesDistances(firstFingerprint, secondFingerprint):
    totalDistance=0
    for i in range (len(firstFingerprint)):
        totalDistance+=hamming_distance(firstFingerprint[i],secondFingerprint[i])
    return(totalDistance)



def hamming_distance(string1, string2):
    shortestLength = min(len(string1),len(string2))
    dist_counter = abs(len(string1)-len(string2))
    for n in range(shortestLength):
        if string1[n] != string2[n]:
            dist_counter += 1
    return dist_counter


sortFile("bigFileHttp.txt")
