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

#Read from static tag file
tagFile = open('/Users/callumc/SpeechProject/Project/tagList.txt', 'r')
tagList = []
maleList = []
femaleList = []
callerList = []
receiverList = []

#Template for data storage
for tag in tagFile:
	#Stores tag and it's bin
	tagStoreMASTER = []
	tagStoreMALE = []
	tagStoreFEMALE = []
	tagStoreCALLER = []
	tagStoreRECEIVER = []
	#Will store all data for said tag
	dataStoreMASTER = []
	dataStoreMALE = []
	dataStoreFEMALE = []
	dataStoreCALLER = []
	dataStoreRECEIVER = []
	#Strips newline chars
	tagFinal = tag.rstrip('\n')

	#Store in correct form
	tagStoreMASTER.append(tagFinal)
	tagStoreMASTER.append(dataStoreMASTER)
	tagStoreMALE.append(tagFinal)
	tagStoreMALE.append(dataStoreMALE)
	tagStoreFEMALE.append(tagFinal)
	tagStoreFEMALE.append(dataStoreFEMALE)
	tagStoreCALLER.append(tagFinal)
	tagStoreCALLER.append(dataStoreCALLER)
	tagStoreRECEIVER.append(tagFinal)
	tagStoreRECEIVER.append(dataStoreRECEIVER)

	#Save this template into each list
	tagList.append(tagStoreMASTER)
	maleList.append(tagStoreMALE)
	femaleList.append(tagStoreFEMALE)
	callerList.append(tagStoreCALLER)
	receiverList.append(tagStoreRECEIVER)

tagFile.close()


fileNames = glob.glob("/Users/callumc/SpeechProject/Project/vocalizationcorpus/newData/extraction/gdata/*.gdata")

#Process a single file at a time
#Splitting all extracted values at a time in nested loop
for curFile in fileNames:
	#Gender check
	isMale = True;
	#Check if male or female
	if (curFile[-12:-11] == "F"):
		isMale = False;
	else:
		isMale = True;

	#Caller/Receiver check
	isCaller = True;
	if (curFile[-8:-7] == "R"):
		isCaller = False;
	else:
		isCaller = True;

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


		#Add to master list
		tagList[i][1].append(calculatedNumber)

		#Add to male/female list
		if (isMale == True):
			maleList[i][1].append(calculatedNumber)
		else:
			femaleList[i][1].append(calculatedNumber)

		#Add to caller/receiver list
		if (isCaller == True):
			callerList[i][1].append(calculatedNumber)
		else:
			receiverList[i][1].append(calculatedNumber)

		i = i + 1

dataFile.close()


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
		print ""

		userChoice = raw_input("#")

		if userChoice == "feat":
			featureList()
		elif userChoice == "devstatsgender":
			statsToCSV("gender")
		elif userChoice == "devstatscaller":
			statsToCSV("caller")

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
	return

mainMenu()
exit()
