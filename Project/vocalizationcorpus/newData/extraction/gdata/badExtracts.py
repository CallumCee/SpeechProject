import os

inFile = open('/Users/callumc/SpeechProject/Project/failedExtracts.txt', 'r')
failedFiles = []

for readLine in inFile:
	failedFiles.append(readLine.rstrip('\n'))

inFile.close()

for curFile in failedFiles:
	os.system("rm /Users/callumc/SpeechProject/Project/vocalizationcorpus/newData/extraction/gdata/" + curFile)