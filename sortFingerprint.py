import time


def sortFile(fileLocation):
    listOfFingerprints = ["liste contenant toutes fingerprints differentes"]
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
    print(numberOfsameFingerprint)
    file.close()


def hamming_distance(string1, string2):
    shortestLength = min(len(string1),len(string2))
    dist_counter = abs(len(string1)-len(string2))
    for n in range(shortestLength):
        if string1[n] != string2[n]:
            dist_counter += 1
    return dist_counter


sortFile("bigFileHttp.txt")
