import wave
import csv
import sys

#sys.argv[1]

#read from file
fileString = sys.argv[1]
dataFile = open(fileString, 'r')

myAttributes = []


for line in dataFile:
	lineData = line.split()
	if len(lineData) == 0:
		continue
	if lineData[0] == '@attribute':
		myAttributes.append(lineData[1])
	if "'unknown'" in lineData[0]:
		rawValues = lineData[0]


dataFile.close()


myValues = rawValues.split(',')

newString = fileString[:-7]
newString = newString + 'gdata'

writeFile = open(newString, 'w')

i = 0
while i < len(myAttributes):
	writeFile.write(myAttributes[i] + "," + myValues[i] + '\n')
	i = i + 1

writeFile.close()


