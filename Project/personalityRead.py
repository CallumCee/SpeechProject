import csv
import numpy as np

'''
MOVING CSV DATA INTO LISTS TO BE PROCESSED
TODO: CLEAN CODE INTO LOOPS, REMOVE REPETITION
'''

#Changes the format to match that of the files
#Makes data matching easier later
def formatID(oldID):
	newID = oldID[1:3] + oldID[4]
	return newID

def fileRead(fileName, startPos):
	#create 5 storage lists
	#raw storage is used when working out the median value
	aStorage = []
	aRaw = []
	bStorage = []
	bRaw = []
	cStorage = []
	cRaw = []
	dStorage = []
	dRaw = []
	eStorage = []
	eRaw = []

	csvfile = open(fileName, 'rb')
	reader = csv.reader(csvfile)
	next(reader,)
	for row in reader:
		#reformat the tag
		tag = formatID(row[0])
		#add the data and tag to each list
		aStorage.append([tag, int(row[startPos])])
		bStorage.append([tag, int(row[startPos+1])])
		cStorage.append([tag, int(row[startPos+2])])
		dStorage.append([tag, int(row[startPos+3])])
		eStorage.append([tag, int(row[startPos+4])])
		#add to the raw storage
		aRaw.append(int(row[startPos]))
		bRaw.append(int(row[startPos+1]))
		cRaw.append(int(row[startPos+2]))
		dRaw.append(int(row[startPos+3]))
		eRaw.append(int(row[startPos+4]))

	csvfile.close()

	#find median of each list
	aMedian = np.median(aRaw)
	bMedian = np.median(bRaw)
	cMedian = np.median(cRaw)
	dMedian = np.median(dRaw)
	eMedian = np.median(eRaw)

	#create (upper,lower) & upper & lower
	aFinal = []
	aUpper = []
	aLower = []
	bFinal = []
	bUpper = []
	bLower = []
	cFinal = []
	cUpper = []
	cLower = []
	dFinal = []
	dUpper = []
	dLower = []
	eFinal = []
	eUpper = []
	eLower = []

	#Deal with A
	for entry in aStorage:
		if (entry[1] >= aMedian):
			aUpper.append(entry[0])
		else:
			aLower.append(entry[0])

	#Deal with B
	for entry in bStorage:
		if (entry[1] >= bMedian):
			bUpper.append(entry[0])
		else:
			bLower.append(entry[0])

	#Deal with C
	for entry in cStorage:
		if (entry[1] >= cMedian):
			cUpper.append(entry[0])
		else:
			cLower.append(entry[0])

	#Deal with D
	for entry in dStorage:
		if (entry[1] >= dMedian):
			dUpper.append(entry[0])
		else:
			dLower.append(entry[0])

	#Deal with E
	for entry in eStorage:
		if (entry[1] >= eMedian):
			eUpper.append(entry[0])
		else:
			eLower.append(entry[0])

	#append these lists to the master lists
	aFinal.append(aUpper)
	aFinal.append(aLower)
	bFinal.append(bUpper)
	bFinal.append(bLower)
	cFinal.append(cUpper)
	cFinal.append(cLower)
	dFinal.append(dUpper)
	dFinal.append(dLower)
	eFinal.append(eUpper)
	eFinal.append(eLower)

	#create master list for returning
	masterList = []

	#add the final lists to the master
	masterList.append(aFinal)
	masterList.append(bFinal)
	masterList.append(cFinal)
	masterList.append(dFinal)
	masterList.append(eFinal)

	return masterList
	
def getOENAC():

	OENAClist = fileRead('q_personality.csv', 11)

	return OENAClist

def getCAODI():

	CAODIlist = fileRead('q_conflict.csv', 36)

	return CAODIlist





