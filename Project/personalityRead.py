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

def getOENAC():
	#Create storage lists in order they appear in csv file
	#Raw storage for easy working with the median
	Ostorage = [] 
	Oraw = []
	Estorage = [] 
	Eraw = []
	Nstorage = [] 
	Nraw = []
	Astorage = [] 
	Araw = []
	Cstorage = [] 
	Craw = []

	#Read the csv files into python lists
	csvfile = open('q_personality.csv', 'rb')
	reader = csv.reader(csvfile)
	next(reader,)
	for row in reader:
		#Reformat the tag
	    tag = formatID(row[0])
	    #Add the data and tag to each list
	    Ostorage.append([tag, int(row[11])])
	    Estorage.append([tag, int(row[12])])
	    Nstorage.append([tag, int(row[13])])
	    Astorage.append([tag, int(row[14])])
	    Cstorage.append([tag, int(row[15])])
	    #Add to the raw storage
	    Oraw.append(int(row[11]))
	    Eraw.append(int(row[12]))
	    Nraw.append(int(row[13]))
	    Araw.append(int(row[14]))
	    Craw.append(int(row[15]))

	csvfile.close()

	#Find median of each list
	Omedian = np.median(Oraw)
	Emedian = np.median(Eraw)
	Nmedian = np.median(Nraw)
	Amedian = np.median(Araw)
	Cmedian = np.median(Craw)

	#Create (upper,lower) & upper & lower
	Ofinal = []
	Oupper = []
	Olower = []
	Efinal = []
	Eupper = []
	Elower = []
	Nfinal = []
	Nupper = []
	Nlower = []
	Afinal = []
	Aupper = []
	Alower = []
	Cfinal = []
	Cupper = []
	Clower = []

	#Deal with Openness
	for entry in Ostorage:
		if (entry[1] >= Omedian):
			Oupper.append(entry[0])
		else:
			Olower.append(entry[0])

	#Deal with Extraversion
	for entry in Estorage:
		if (entry[1] >= Emedian):
			Eupper.append(entry[0])
		else:
			Elower.append(entry[0])

	#Deal with Neuroticism
	for entry in Nstorage:
		if (entry[1] >= Nmedian):
			Nupper.append(entry[0])
		else:
			Nlower.append(entry[0])

	#Deal with Agreeableness
	for entry in Astorage:
		if (entry[1] >= Amedian):
			Aupper.append(entry[0])
		else:
			Alower.append(entry[0])

	#Deal with Concientiousness
	for entry in Cstorage:
		if (entry[1] >= Cmedian):
			Cupper.append(entry[0])
		else:
			Clower.append(entry[0])

	#Append these lists to the master lists for each of OENAC
	Ofinal.append(Oupper)
	Ofinal.append(Olower)
	Efinal.append(Eupper)
	Efinal.append(Elower)
	Nfinal.append(Nupper)
	Nfinal.append(Nlower)
	Afinal.append(Aupper)
	Afinal.append(Alower)
	Cfinal.append(Cupper)
	Cfinal.append(Clower)

	#Create master list for returning
	OENACmaster = []

	#Add the final lists to the master
	OENACmaster.append(Ofinal)
	OENACmaster.append(Efinal)
	OENACmaster.append(Nfinal)
	OENACmaster.append(Afinal)
	OENACmaster.append(Cfinal)

	return OENACmaster







