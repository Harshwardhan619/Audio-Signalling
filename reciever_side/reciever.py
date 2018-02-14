import os
import re
import sys
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


# Recording sound
def recording(time):

	fs = 44100

	duration = time  # seconds
	myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
	sd.default.samplerate = fs
	sd.default.channels = 2
	myrecording = sd.rec(int(duration * fs))
	sd.wait()

	#print(myrecording)

	#data = np.random.uniform(-1,1,44100) # 44100 random samples between -1 and 1
	scaled = np.int16(myrecording/np.max(np.abs(myrecording)) * 32767)
	write("test.wav", 44100, scaled)

#Playing sound 
def playsound(bitstring):
	for bit in bitstring:
		if bit == '1':
			os.system('paplay Networks\ 1.wav')
		else:
			os.system('paplay Networks\ 2.wav')

def detecterror(string):
	
	string1= string[:-9]
	string2= string1

	length=len(string1)
	paritybits= string[-9:]
	if length <20:
		string1= string1+ '0'*(20-length)
	array= [int(i) for i in list(string1)]
	mat= np.matrix(array)
	mat.resize(4,5)
	row_sums= mat.sum(axis=1)
	column_sums= mat.sum(axis=0)

	# print(row_sums,column_sums)
	# print(paritybits)
	row_faults=0
	row=-1
	column=-1
	for i in range(4):
		if row_sums.item(i)%2 !=int(paritybits[i]):
			row=i
			row_faults+=1

	column_faults=0
	for i in range(4,9):
		if column_sums.item(i-4)%2!=int(paritybits[i]):
			column=i-4
			
			column_faults+=1
			# print(i-m+1, "column")
	# print(row_faults,column_faults)
	if row_faults==1 and column_faults==1:
		if array[row*5+column]==1:
			array[row*5+column]=0
		else:
			array[row*5+column]=1
		print(array)
		print("error is corrected in: ",row*5+column+1)
		string="".join([str(i) for i in array])
		string= string[:length]
		return string
		
	if row_faults>0 or column_faults>0:
		print("error has occurred in: ", string1[:length])
		return "-1"
	else:
		return string2


	# string1= string[:-9]
	# length=len(string1)
	# paritybits= string[-9:]
	# if length <20:
	# 	string1= string1+ '0'*(20-length)
	# array= [int(i) for i in list(string1)]
	# mat= np.matrix(array)
	# print(mat)
	# mat.resize(4,5)
	# row_sums= mat.sum(axis=1)
	# column_sums= mat.sum(axis=0)

	# # print(row_sums,column_sums)
	# # print(paritybits)
	# row_faults=0
	# row=-1
	# column=-1
	# for i in range(4):
	# 	if row_sums.item(i)%2 !=int(paritybits[i]):
	# 		row=i
	# 		row_faults+=1

	# column_faults=0
	# for i in range(4,9):
	# 	if column_sums.item(i-4)%2!=int(paritybits[i]):
	# 		column=i-4
			
	# 		column_faults+=1
	# 		# print(i-m+1, "column")
	# # print(row_faults,column_faults)
	# if row_faults>0 or column_faults>0:
	# 	print("error has occurred")
	# 	return "-1"
	# else:
	# 	return string1

def decoder(inp):
	[a,b]=re.subn('01111110',' ',inp)
	[c,d]=re.subn('111110','11111',a)
	return c.split(' ')



fullrecord = 27

halfrecord = 15
sleeptime = 2
recieved = 0
playsound("1")
print("Program Started, Press enter to continue")

temp1=input()
print("Strating Recording for: ", fullrecord, " seconds...")
recording(fullrecord)
print("Done Recording, Now Processing")
s=os.popen('bash script.sh').read()

print("Recieved text is: ", s)

s = decoder(s)
print(s)
errordetect = ["0"]*2
errordetect[0] = detecterror(s[0])
errordetect[1] = detecterror(s[1])

print(errordetect)

while recieved !=1:

	if errordetect[0]!= "-1" and errordetect[1] !="-1":
		print("Correct sequence recieved: ", errordetect)
		print("Press enter key to send an ACK")
		temp1=input()

		recieved=1
		os.system("paplay Networks\ 1.wav")
		time.sleep(sleeptime)

		playsound("11")
		print("Recieved Completed")
		print("Correct sequence: ", errordetect)

	else:
		print("Incorrect sequence recieved. Press enter key to send an NACK")
		temp1=input()

		os.system("paplay Networks\ 1.wav")
		time.sleep(sleeptime)

		if errordetect[0] == "-1" and errordetect[1] =="-1":
			playsound("001")
			print("NACK send, Press enter to start recording of Retransmission")
			
			temp1=input()
			print("Now Recording ...")
			recording(fullrecord)
			s=os.popen('bash script.sh').read()
			s = decoder(s)
			print(s)
			errordetect = ["0"]*2
			errordetect[0] = detecterror(s[0])
			errordetect[1] = detecterror(s[1])

		elif errordetect[0] == "-1":
			playsound("00")
			print("NACK send, Press enter to start recording of Retransmission")

			temp1=input()
			print("Now Recording ...")
			recording(halfrecord)
			s=os.popen('bash script.sh').read()
			s = decoder(s)
			errordetect[0] = detecterror(s[0])


		elif errordetect[1] == "-1":
			playsound("01")
			print("NACK send, Press enter to start recording of Retransmission")

			temp1=input()
			print("Now Recording ...")
			recording(halfrecord)
			s = decoder(s)
			errordetect[1] = detecterror(s[1])


		# Print("NACK send, Press enter to start recording of Retransmission")

		# temp1=input()
		# print("Now Recording ...")

		# recording(20)


#waiting for ACK


