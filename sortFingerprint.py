import xlsxwriter
import sys

def main(aFile):
    return sortFile(aFile)


####
# Take a file as input and give an xlsx as output. This xlsx gives all the distances between the fingerprints. The current distance used is the hamming distance for
# now. 
####

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
    listOfFingerprints.pop(0)
    numberOfsameFingerprint.pop(0)
    for x in listOfFingerprints:
        listOfSplitedFingerprints.append(x.split('|'))
    listOfDistances=calculateDistanceBetweenFingerprints(listOfSplitedFingerprints)
    writeInXlsx(listOfDistances,listOfFingerprints)
    file.close()

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

###   
# calculate the complete distance between two fingerprints. 
###

def sumSubcategoriesDistances(firstFingerprint, secondFingerprint):
    totalDistance=0
    for i in range (len(firstFingerprint)):
        totalDistance+=hamming_distance(firstFingerprint[i],secondFingerprint[i])
    return(totalDistance)

###
# Write in an xlsx file the distances associated to a list of Fringerprints. 
###

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
        



###
# determine the hamming_distance between two fingerprints. 
###
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
main(sys.argv[1]) 
