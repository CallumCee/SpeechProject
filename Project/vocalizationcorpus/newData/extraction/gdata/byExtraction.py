import os
import csv

masterStorage = []

headerFile = open('/Users/callumc/Desktop/Uni/Project/vocalizationcorpus/newData/extraction/gdata/S0001F1.gdata', 'r')
#Read the first file so we can extract the headers for storage
csvReader = csv.reader(headerFile)
next(csvReader) #Skips the header file
for row in csvReader:
	headerStorage = []
	headerStorage.append(row[0])
	masterStorage.append(headerStorage)

headerFile.close()

#Store all the file names to extract from
fileNames = []
for file in os.listdir('/Users/callumc/Desktop/Uni/Project/vocalizationcorpus/newData/extraction/gdata'):
    if file.endswith(".gdata"):
    	fileNames.append(file)


#Store all the values from each file
for entry in fileNames:
	currentFile = open(entry, 'r')
	csvReader = csv.reader(currentFile)
	next(csvReader)

	i = 0
	for row in csvReader:
		masterStorage[i].append(row[1])
		i = i + 1

	currentFile.close()

#Write to individual files
for entry in masterStorage:
	outString = entry[0] + '.valuelist'

	writeFile = open(outString, 'w')

	i = 1
	while i < len(entry):
		writeFile.write(entry[i] + '\n')
		i = i + 1

	writeFile.close()

