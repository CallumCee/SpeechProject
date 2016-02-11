import csv
import wave

def cutWaveFile(row, instance, timeA, timeB, masterWave):
	#Name of the wav file to edit
		fileFind = 'data/' + row[0] + '.wav'

		#Caller/Reciever & Person ID
		roleInfo = '_' + row[1][1:3] + row[1][4]
		#Name of the wav file to be created
		#((File name + Gender letter + Instance))
		fileWrite = 'newData/' + row[0] + row[2][0] + roleInfo + str(instance) + '.wav'
		curWave = wave.open(fileFind, 'rb')
		newWave = wave.open(fileWrite, 'wb')

		#Start and end times
		t0, t1 = float(timeA), float(timeB)
		s0, s1 = int(t0*curWave.getframerate()), int(t1*curWave.getframerate())

		#Discard before
		curWave.readframes(s0)
		fillerAudio = curWave.readframes(s1 - s0)

		#Set parameters? - **
		newWave.setparams(curWave.getparams())
		newWave.writeframes(fillerAudio)
		masterWave.writeframes(fillerAudio)

		#Close read/write
		curWave.close()
		newWave.close()
		print 'file ' + fileWrite + ' was created'


#labels file contains information on corpus .wav files
dataFile = open('labels.txt')

#Master file setup
masterWave = wave.open('newData/masterWave.wav', 'wb')
masterWave.setparams((1,2,16000,176000,'NONE','not compressed'))

try:
	csvReader = csv.reader(dataFile)
	#Skips the header
	next(csvReader)

	for row in csvReader:
		#Set params
		instance = 1
		timeA, timeB = row[5], row[6]
		rowLen = len(row)

		if row[4] == 'filler':
			cutWaveFile(row, instance, timeA, timeB, masterWave)

		#if no more then continue to next loop
		if rowLen <= 7:
			continue

		if row[7] == 'filler':
			instance += 1
			timeA, timeB = row[8], row[9]
			cutWaveFile(row, instance, timeA, timeB, masterWave)

		if rowLen <= 10:
			continue

		if row[10] == 'filler':
			instance += 1
			timeA, timeB = row[11], row[12]
			cutWaveFile(row, instance, timeA, timeB, masterWave)

		
finally:
	dataFile.close()
	masterWave.close()
	print 'file newData/masterWave.wav was created'

