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
import sys
import csv
import glob
import math
import numpy

tagFile = open('/Users/callumc/Desktop/Uni/Project/tagList.txt', 'r')
tagList = []

for tag in tagFile:
	#Stores tag and it's bin
	tagStore = []
	#Will store all data for said tag
	dataStore = []
	#Strips newline chars
	tagFinal = tag.rstrip('\n')

	tagStore.append(tagFinal)
	tagStore.append(dataStore)

	tagList.append(tagStore)

tagFile.close()


fileNames = glob.glob("/Users/callumc/Desktop/Uni/Project/vocalizationcorpus/newData/extraction/gdata/*.gdata")

for curFile in fileNames:
	#Open the file
	dataFile = open(curFile, 'r')
	#Skip the first line (headers)
	dataFile.readline()
	i=0
	while i < 62:
		curLine = dataFile.readline()
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



		tagList[i][1].append(calculatedNumber)

		i = i + 1

dataFile.close()

i=0
while i < len(tagList):
	print str(i + 1) + ': ' + tagList[i][0]
	i = i + 1

print ''
print ''
currentGraphNumber = raw_input("Enter desired graph number: ")
currentGraphNumber = int(currentGraphNumber) - 1

# data
graphData = tagList[currentGraphNumber][1]
# mean of distribution
mu = sum(graphData) / float(len(graphData))
# standard deviation of distribution
sigma = numpy.std(graphData)

#Standard number of bins for datapyt
num_bins = 50

bin_choice = raw_input("Enter bin size: 'more' / 'norm' / 'less' \n")

if bin_choice == 'more':
	num_bins = num_bins * 2
elif bin_choice == 'less':
	num_bins = num_bins / 2

# the histogram of the data
n, bins, patches = plt.hist(tagList[currentGraphNumber][1], num_bins, facecolor='green', alpha=0.5)
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y,'r--')
plt.xlabel('Value of ' + tagList[currentGraphNumber][0])
plt.ylabel('Frequency')
plt.title('Histogram of ' + tagList[currentGraphNumber][0])

# Tweak spacing to prevent clipping of ylabel
plt.subplots_adjust(left=0.15)
plt.show()