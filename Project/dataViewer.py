"""
Demo of the histogram (hist) function with a few features.

In addition to the basic histogram, this demo shows a few optional features:

    * Setting the number of data bins
    * The ``normed`` flag, which normalizes bin heights so that the integral of
      the histogram is 1. The resulting histogram is a probability density.
    * Setting the face color of the bars
    * Setting the opacity (alpha value).

"""
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.stats as spstats
import sys
import csv
import glob
import math
import numpy
import personalityRead as pRead


#Does ANOVA statistical analysis
def signStats(d1, d2, all):
	#Return list where (F Value, P Value, F Critical)
	statOutList = []

	fVal, pVal = spstats.f_oneway(d1, d2)
	fCrit = spstats.distributions.f.ppf(0.95 , 1, len(all)) #0.95 = when 0.05p

	statOutList.append(fVal)
	statOutList.append(pVal)
	statOutList.append(fCrit)

	return statOutList


#UI - main menu
def mainMenu():
	#Set initial as blank
	userChoice = ""

	#Loop until exit
	while (userChoice != "exit"):
		print ""
		print "HISTOGRAM PLOT & ANALYSIS"
		print "~+~+~+~+~+~+~+~+~+~+~+~+~+~+"
		print "Type 'feat' to select from the feature list"
		print "Type 'exit' to exit the program"
		print "~+~+~+~+~+~+~+~+~+~+~+~+~+~+"
		print "Type 'devstatsgender' for analysis csv output (gender focus)"
		print "Type 'devstatscaller' for analysis csv output (caller/receiver focus)"
		print "Type 'devstatsfinal' for analysis csv output (OENAC final)"
		print ""

		userChoice = raw_input("#")

		if userChoice == "feat":
			featureList()
		elif userChoice == "devstatsgender":
			statsToCSV("gender")
		elif userChoice == "devstatscaller":
			statsToCSV("caller")
		elif userChoice == "devstatsfinal":
			createMasterCSV()

	if (userChoice == "exit"):
		exit()

	return

#List of extracted features
def featureList():
	i=0
	while i < len(tagList):
		print str(i + 1) + ': ' + tagList[i][0]
		i = i + 1

	print ''
	print ''
	currentGraphNumber = raw_input("Enter desired graph number: ")
	currentGraphNumber = int(currentGraphNumber) - 1
	advFeatureChoice(currentGraphNumber)
	return

#Grouping data and obtaining stats/histogram
def advFeatureChoice(graphNumber):
	print ""
	print "Type 'all' to display data from all participants"
	print "Type 'male' to display only data from male participants"
	print "Type 'female' to display only data from female participants"
	print "Type 'caller' to display data from caller participants"
	print "Type 'receiver' to display data from receiver participants"
	userChoiceDataSet = raw_input("#")

	userChoiceFunction = ""
	while (userChoiceFunction != "menu"):
		print ""
		print "Type 'hist' for a histogram of the data"
		print "Type 'stats' for some basic statistics of this data"
		print "Type 'menu' to return to the main menu"

		userChoiceFunction = raw_input("#")

		if (userChoiceFunction == "hist"):
			drawHist(graphNumber, userChoiceDataSet)
		elif (userChoiceFunction == "stats"):
			basicStats(graphNumber, userChoiceDataSet)

	mainMenu()
	return

#Creates the histogram to display
def drawHist(graphNumber, dataChoice):

	#data
	if dataChoice == "male":
		graphData = maleList[graphNumber]
		print 'Male data selected'
	elif dataChoice == "female":
		graphData = femaleList[graphNumber]
		print 'Female data selected'
	elif dataChoice == "caller":
		graphData = callerList[graphNumber]
		print 'Caller data selected'
	elif dataChoice == "receiver":
		graphData = receiverList[graphNumber]
		print 'Receiver data selected'
	else:
		graphData = tagList[graphNumber]
		print 'All data selected'


	# mean of distribution
	mu = sum(graphData[1]) / float(len(graphData[1]))
	# standard deviation of distribution
	sigma = numpy.std(graphData[1])

	#Standard number of bins for datapyt
	num_bins = 50

	bin_choice = raw_input("Enter bin size: 'more' / 'norm' / 'less' \n")

	if bin_choice == 'more':
		num_bins = num_bins * 2
	elif bin_choice == 'less':
		num_bins = num_bins / 2

	# the histogram of the data
	plt.hist(graphData[1], num_bins, facecolor='green', alpha=0.5)

	plt.xlabel('Value of ' + graphData[0])
	plt.ylabel('Frequency')
	plt.title('Histogram of ' + graphData[0])

	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	plt.show()
	return

#Produces some statistics for the given data set
def basicStats(graphNumber, dataChoice):
	stringTitle = ""
	#data
	if dataChoice == "male":
		graphData = maleList[graphNumber]
		stringTitle =  "Male Data"
	elif dataChoice == "female":
		graphData = femaleList[graphNumber]
		stringTitle = "Female Data"
	elif dataChoice == "caller":
		graphData = callerList[graphNumber]
		stringTitle = "Caller Data"
	elif dataChoice == "receiver":
		graphData = receiverList[graphNumber]
		stringTitle = "Receiver Data"
	else:
		graphData = tagList[graphNumber]
		stringTitle = "All Data"

	print ""
	print "BASIC STATISTICS - " + graphData[0] + " - " + stringTitle
	print "+~+~+~+~+~+~+~+~+~+"
	print "The mean value is: " + str(np.mean(graphData[1]))
	print "The median value is: " + str(np.median(graphData[1]))
	print "The variance is: " + str(np.var(graphData[1]))
	print "The minimum value is: " + str(np.amin(graphData[1]))
	print "The maximum value is: " + str(np.amax(graphData[1]))
	print "The number of data items is: " + str(len(graphData[1]))
	if dataChoice == "all":
		signData = signStats(maleList[graphNumber][1], femaleList[graphNumber][1], tagList[graphNumber][1])
		print "ANOVA F Value is: " + str(signData[0])
		print "ANOVA P Value is: " + str(signData[1])
		print "ANOVA F Critical (p=0.05) is: " + str(signData[2])
	print ""

	return

#Output data set stats to a CSV file
def statsToCSV(datatype):
	#Set up the type of out
	if (datatype == "gender"):
		a = "male"
		b = "female"
		aList = maleList
		bList = femaleList
	else:
		a = "caller"
		b = "receiver"
		aList = callerList
		bList = receiverList

	outFile = open('/Users/callumc/SpeechProject/Project/stats' + a + b + '.csv', 'w')

	headerLine = 'extracted_feature, '+a+'_mean, '+b+'_mean, all_mean, '+a+'_median, '+b+'_median, all_median,' \
					' '+a+'_variance, '+b+'_variance, all_variance, '+a+'_stdev, '+b+'_stdev, all_stdev,' \
					' anova_Fval, anova_Fcrit5, anova_Pval'

	headerLine += '\n'

	outFile.write(headerLine)

	i=0
	while (i < 62):
		#extracted_feature
		lineOut = tagList[i][0]
		#means
		lineOut += ", " + str(np.mean(aList[i][1]))
		lineOut += ", " + str(np.mean(bList[i][1]))
		lineOut += ", " + str(np.mean(tagList[i][1]))
		#medians
		lineOut += ", " + str(np.median(aList[i][1]))
		lineOut += ", " + str(np.median(bList[i][1]))
		lineOut += ", " + str(np.median(tagList[i][1]))
		#variances
		lineOut += ", " + str(np.var(aList[i][1]))
		lineOut += ", " + str(np.var(bList[i][1]))
		lineOut += ", " + str(np.var(tagList[i][1]))
		#standard deviations
		lineOut += ", " + str(np.std(aList[i][1]))
		lineOut += ", " + str(np.std(bList[i][1]))
		lineOut += ", " + str(np.std(tagList[i][1]))
		#anova calculations
		signData = signStats(aList[i][1], bList[i][1], tagList[i][1])
		#anova F value
		lineOut += ", " + str(signData[0])
		#anova F critical value
		lineOut += ", " + str(signData[2])
		#anova P value
		lineOut += ", " + str(signData[1])

		#newline char
		lineOut += '\n'

		outFile.write(lineOut)
		i = i + 1

	outFile.close()
	print 'Created CSV for ' + datatype
	return

#For main CSV output, checks if the p value is significant
def outputSignificance(pdata):
	outstring = ""
	if (pdata <= 0.05):
			outstring = "*"
	if (pdata <= 0.01):
			outstring = "**"
	return outstring

#Outputs the main CSV for final analysis
def createMasterCSV():
	outFile = open('/Users/callumc/SpeechProject/Project/completedData.csv', 'w')

	headerLine = 'extracted_feature, gender_anova_Fval, gender_anova_Pval, call-rece_anova_Fval, call-rece_anova_Pval, ' \
					'O_anova_Fval, O_anova_Pval, E_anova_Fval, E_anova_Pval, N_anova_Fval, N_anova_Pval, ' \
					'A_anova_Fval, A_anova_Pval, C_anova_Fval, C_anova_Pval, ConfC_anova_Fval, ConfC_anova_Pval, ' \
					'ConfA_anova_Fval, ConfA_anova_Pval, ConfO_anova_Fval, ConfO_anova_Pval, ConfD_anova_Fval, ConfD_anova_Pval, ' \
					'ConfI_anova_Fval, ConfI_anova_Pval'

	headerLine += '\n'

	outFile.write(headerLine)

	i=0
	while (i < 62):
		#extracted_feature
		lineOut = tagList[i][0]

		#gender vals
		genderData = signStats(maleList[i][1], femaleList[i][1], tagList[i][1])
		lineOut += ", " + str(genderData[0]) #Fval
		lineOut += ", " + str(genderData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(genderData[1])
		if (signStr != ""):
			lineOut += signStr

		#call-rece vals
		callreceData = signStats(callerList[i][1], receiverList[i][1], tagList[i][1])
		lineOut += ", " + str(callreceData[0]) #Fval
		lineOut += ", " + str(callreceData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(callreceData[1])
		if (signStr != ""):
			lineOut += signStr

		#OENAC vals
		#Openness
		OData = signStats(upperOList[i][1], lowerOList[i][1], tagList[i][1])
		lineOut += ", " + str(OData[0]) #Fval
		lineOut += ", " + str(OData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(OData[1])
		if (signStr != ""):
			lineOut += signStr

		#Extraversion
		EData = signStats(upperEList[i][1], lowerEList[i][1], tagList[i][1])
		lineOut += ", " + str(EData[0]) #Fval
		lineOut += ", " + str(EData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(EData[1])
		if (signStr != ""):
			lineOut += signStr

		#Neuroticism
		NData = signStats(upperNList[i][1], lowerNList[i][1], tagList[i][1])
		lineOut += ", " + str(NData[0]) #Fval
		lineOut += ", " + str(NData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(NData[1])
		if (signStr != ""):
			lineOut += signStr

		#Agreeableness
		AData = signStats(upperAList[i][1], lowerAList[i][1], tagList[i][1])
		lineOut += ", " + str(AData[0]) #Fval
		lineOut += ", " + str(AData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(AData[1])
		if (signStr != ""):
			lineOut += signStr

		#Concientiousness
		CData = signStats(upperCList[i][1], lowerCList[i][1], tagList[i][1])
		lineOut += ", " + str(CData[0]) #Fval
		lineOut += ", " + str(CData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(CData[1])
		if (signStr != ""):
			lineOut += signStr

		#Compromising
		ConfCData = signStats(upperConfCList[i][1], lowerConfCList[i][1], tagList[i][1])
		lineOut += ", " + str(ConfCData[0]) #Fval
		lineOut += ", " + str(ConfCData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(ConfCData[1])
		if (signStr != ""):
			lineOut += signStr

		#Avoiding
		ConfAData = signStats(upperConfAList[i][1], lowerConfAList[i][1], tagList[i][1])
		lineOut += ", " + str(ConfAData[0]) #Fval
		lineOut += ", " + str(ConfAData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(ConfAData[1])
		if (signStr != ""):
			lineOut += signStr

		#Obliging
		ConfOData = signStats(upperConfOList[i][1], lowerConfOList[i][1], tagList[i][1])
		lineOut += ", " + str(ConfOData[0]) #Fval
		lineOut += ", " + str(ConfOData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(ConfOData[1])
		if (signStr != ""):
			lineOut += signStr

		#Dominating
		ConfDData = signStats(upperConfDList[i][1], lowerConfDList[i][1], tagList[i][1])
		lineOut += ", " + str(ConfDData[0]) #Fval
		lineOut += ", " + str(ConfDData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(ConfDData[1])
		if (signStr != ""):
			lineOut += signStr

		#Compromising
		ConfIData = signStats(upperConfIList[i][1], lowerConfIList[i][1], tagList[i][1])
		lineOut += ", " + str(ConfIData[0]) #Fval
		lineOut += ", " + str(ConfIData[1]) #Pval
		#Check for significance
		signStr = outputSignificance(ConfIData[1])
		if (signStr != ""):
			lineOut += signStr

		#newline char
		lineOut += '\n'

		outFile.write(lineOut)
		i = i + 1

	outFile.close()
	print 'Created CSV for OENAC (final)'
	return

#Creates a tag & data storage lists
def dataStoreFactory(tag):
	tagStore = []
	dataStore = []

	tagStore.append(tag.rstrip('\n'))
	tagStore.append(dataStore)

	return tagStore

#Checks if filename matches the given string to see if data belongs to a group
def checkMembership(position, matchCheck, checkType):
	isMember = True

	#checkType 0 is a string match, 1 is for a 'in list check'
	if (checkType == 0):
		if (position == matchCheck):
			isMember = False
	else:
		if (position in matchCheck):
			isMember = False

	return isMember

#Adds the data to locA/locB depending on isMember
def dataToList(isMember, locA, locB, num):
	if (isMember == True):
		locA.append(num)
	else:
		locB.append(num)

	return

#Test fn for min/max finding of filenames
def myMinMax(curList):
	#Set min/max to the first elements of the list
	themin = curList[0][1]
	themax = curList[0][1]
	minEntry = curList[0]
	maxEntry = curList[0]

	for entry in curList:
		if (entry[1] < themin):
			themin = entry[1]
			minEntry = entry

		elif (entry[1] > themax):
			themax = entry[1]
			maxEntry = entry

	print minEntry
	print maxEntry

'''
START:	> READ TAG FILE TO OBTAIN FEATURE NAMES
		> CREATE DATA STORAGE BINS FOR EACH ANALYSIS CASE
'''
#Read from static tag file
tagFile = open('/Users/callumc/SpeechProject/Project/tagList.txt', 'r')
tagList = []
#Gender
maleList = []
femaleList = []
#Caller/Receiver
callerList = []
receiverList = []
#OENAC
upperOList = []
lowerOList = []
upperEList = []
lowerEList = []
upperNList = []
lowerNList = []
upperAList = []
lowerAList = []
upperCList = []
lowerCList = []
#CAODI
upperConfCList = []
lowerConfCList = []
upperConfAList = []
lowerConfAList = []
upperConfOList = []
lowerConfOList = []
upperConfDList = []
lowerConfDList = []
upperConfIList = []
lowerConfIList = []

#Import Personality OENAC data from file using personalityRead.py
OENACsort = pRead.getOENAC()

#Import Conflict CAODI data from file using personalityRead.py
CAODIsort = pRead.getCAODI()

#Template for data storage
for tag in tagFile:
	#Stores the tag of the feature and it's data storage bin
	#Master
	tagStoreMASTER = dataStoreFactory(tag)
	#Gender
	tagStoreMALE = dataStoreFactory(tag)
	tagStoreFEMALE = dataStoreFactory(tag)
	#Caller/Receiver
	tagStoreCALLER = dataStoreFactory(tag)
	tagStoreRECEIVER = dataStoreFactory(tag)
	#OENAC
	tagStoreUpperO = dataStoreFactory(tag)
	tagStoreLowerO = dataStoreFactory(tag)
	tagStoreUpperE = dataStoreFactory(tag)
	tagStoreLowerE = dataStoreFactory(tag)
	tagStoreUpperN = dataStoreFactory(tag)
	tagStoreLowerN = dataStoreFactory(tag)
	tagStoreUpperA = dataStoreFactory(tag)
	tagStoreLowerA = dataStoreFactory(tag)
	tagStoreUpperC = dataStoreFactory(tag)
	tagStoreLowerC = dataStoreFactory(tag)
	#CAODI
	tagStoreUpperConfC = dataStoreFactory(tag)
	tagStoreLowerConfC = dataStoreFactory(tag)
	tagStoreUpperConfA = dataStoreFactory(tag)
	tagStoreLowerConfA = dataStoreFactory(tag)
	tagStoreUpperConfO = dataStoreFactory(tag)
	tagStoreLowerConfO = dataStoreFactory(tag)
	tagStoreUpperConfD = dataStoreFactory(tag)
	tagStoreLowerConfD = dataStoreFactory(tag)
	tagStoreUpperConfI = dataStoreFactory(tag)
	tagStoreLowerConfI = dataStoreFactory(tag)

	#Save this template into each list
	tagList.append(tagStoreMASTER)
	#Gender
	maleList.append(tagStoreMALE)
	femaleList.append(tagStoreFEMALE)
	#Caller/Receiver
	callerList.append(tagStoreCALLER)
	receiverList.append(tagStoreRECEIVER)
	#OENAC
	upperOList.append(tagStoreUpperO)
	lowerOList.append(tagStoreLowerO)
	upperEList.append(tagStoreUpperE)
	lowerEList.append(tagStoreLowerE)
	upperNList.append(tagStoreUpperN)
	lowerNList.append(tagStoreLowerN)
	upperAList.append(tagStoreUpperA)
	lowerAList.append(tagStoreLowerA)
	upperCList.append(tagStoreUpperC)
	lowerCList.append(tagStoreLowerC)
	#CAODI
	upperConfCList.append(tagStoreUpperConfC)
	lowerConfCList.append(tagStoreLowerConfC)
	upperConfAList.append(tagStoreUpperConfA)
	lowerConfAList.append(tagStoreLowerConfA)
	upperConfOList.append(tagStoreUpperConfO)
	lowerConfOList.append(tagStoreLowerConfO)
	upperConfDList.append(tagStoreUpperConfD)
	lowerConfDList.append(tagStoreLowerConfD)
	upperConfIList.append(tagStoreUpperConfI)
	lowerConfIList.append(tagStoreLowerConfI)
	

tagFile.close()

'''
	> READ THE DATA IN FROM FILE
	> ADD TO THE CREATED BINS
'''

fileNames = glob.glob("/Users/callumc/SpeechProject/Project/vocalizationcorpus/newData/extraction/gdata/*.gdata")

#Keeps track of cycles for displaying percentage completed
cycleCount = 0
percentageStr = ""

#Min/Max find test code
minmaxList = []

#Process a single file at a time
#Splitting all extracted values at a time in nested loop
for curFile in fileNames:
	#Check if male or female
	isMale = checkMembership(curFile[-12:-11], "F", 0)

	#Caller/Receiver check
	isCaller = checkMembership(curFile[-8:-7], "R", 0)

	#Check if Olower/Oupper
	isOUpper = checkMembership(curFile[-10:-7], OENACsort[0][1], 1)

	#Check if Elower/Eupper
	isEUpper = checkMembership(curFile[-10:-7], OENACsort[1][1], 1)

	#Check if Nlower/Nupper
	isNUpper = checkMembership(curFile[-10:-7], OENACsort[2][1], 1)

	#Check if Alower/Aupper
	isAUpper = checkMembership(curFile[-10:-7], OENACsort[3][1], 1)

	#Check if Clower/Cupper
	isCUpper = checkMembership(curFile[-10:-7], OENACsort[4][1], 1)

	#Check if ConfClower/ConfCupper
	isConfCUpper = checkMembership(curFile[-10:-7], CAODIsort[0][1], 1)

	#Check if ConfClower/ConfCupper
	isConfAUpper = checkMembership(curFile[-10:-7], CAODIsort[1][1], 1)

	#Check if ConfClower/ConfCupper
	isConfOUpper = checkMembership(curFile[-10:-7], CAODIsort[2][1], 1)

	#Check if ConfClower/ConfCupper
	isConfDUpper = checkMembership(curFile[-10:-7], CAODIsort[3][1], 1)

	#Check if ConfClower/ConfCupper
	isConfIUpper = checkMembership(curFile[-10:-7], CAODIsort[4][1], 1)

	#Open the file
	dataFile = open(curFile, 'r')
	#Skip the first line (headers)
	dataFile.readline()
	i=0
	while i < 62:
		curLine = dataFile.readline()

		if (curLine == ''):
			break

		curLine = curLine.split(',')
		curLine[1] = curLine[1].rstrip('\n')

		if curLine[1] == 'nan':
			i = i + 1
			continue

		#split by e to calculate actual value
		numberCalc = curLine[1].split('e')
		numberCalc[0] = float(numberCalc[0])
		numberCalc[1] = float(numberCalc[1])

		calculatedPower = math.pow(10,numberCalc[1])
		calculatedNumber = numberCalc[0]*calculatedPower

		'''TEMP CODE FOR FINDING MINS AND MAXIMUMS WITHOUT
		   HAVING TO REDESIGN THE WHOLE CODE'''

		#Add things here to the temp list
		#Change 0 to the feature number to min/max find
		if (i == 1):
			minmaxList.append([curFile, calculatedNumber])

		''' --- END TEST CODE --- '''

		#Add to master list
		tagList[i][1].append(calculatedNumber)

		#Add to male/female list
		dataToList(isMale, maleList[i][1], femaleList[i][1], calculatedNumber)

		#Add to caller/receiver list
		dataToList(isCaller, callerList[i][1], receiverList[i][1], calculatedNumber)

		#Add to O upper/lower list
		dataToList(isOUpper, upperOList[i][1], lowerOList[i][1], calculatedNumber)

		#Add to E upper/lower list
		dataToList(isEUpper, upperEList[i][1], lowerEList[i][1], calculatedNumber)

		#Add to N upper/lower list
		dataToList(isNUpper, upperNList[i][1], lowerNList[i][1], calculatedNumber)

		#Add to A upper/lower list
		dataToList(isAUpper, upperAList[i][1], lowerAList[i][1], calculatedNumber)

		#Add to C upper/lower list
		dataToList(isCUpper, upperCList[i][1], lowerCList[i][1], calculatedNumber)

		#Add to ConfC upper/lower list
		dataToList(isConfCUpper, upperConfCList[i][1], lowerConfCList[i][1], calculatedNumber)

		#Add to ConfA upper/lower list
		dataToList(isConfAUpper, upperConfAList[i][1], lowerConfAList[i][1], calculatedNumber)

		#Add to ConfO upper/lower list
		dataToList(isConfOUpper, upperConfOList[i][1], lowerConfOList[i][1], calculatedNumber)

		#Add to ConfD upper/lower list
		dataToList(isConfDUpper, upperConfDList[i][1], lowerConfDList[i][1], calculatedNumber)

		#Add to ConfI upper/lower list
		dataToList(isConfIUpper, upperConfIList[i][1], lowerConfIList[i][1], calculatedNumber)

		i = i + 1

	#Displaying progress
	prevString = percentageStr
	cycleCount += 1
	percentageVal = (float(cycleCount) / 2771.0) * 100.0
	percentageStr = str(round(percentageVal, 0))
	if (prevString != percentageStr):
		print percentageStr + "% processed."

#MaxMinWorkoutTestCodeHere
myMinMax(minmaxList)

dataFile.close()

'''
	> COMMENCE THE LUI MENU
'''
mainMenu()
exit()


