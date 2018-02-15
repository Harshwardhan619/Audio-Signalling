import os
import re
import sys
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


# s=os.popen('bash script.sh').read()

# encode sentinel

def encoder(inp):
	[a,b]=re.subn('11111','111110',inp)
	return a
# python encode.py 1000 0000111
def sentinel (str1):
	msg=""
	msg= msg+ encoder(str1[0]) + "01111110" + encoder(str1[1])
	return msg

# 2d-parity
def parity_maker (string):
	length=len(string)
	if length <20:
		string= string+ '0'*(20-length)
	array= [int(i) for i in list(string)]
	mat= np.matrix(array)
	mat.resize(4,5)
	row_sums= mat.sum(axis=1)
	column_sums= mat.sum(axis=0)
	string= string[:length]
	for i in range(4):
		string= string+ str(row_sums.item(i)%2)

	for i in range(5):
		string= string+ str(column_sums.item(i)%2)

	return string


# Recording sound
def recording(time):

	fs = 44100

	duration = time  # seconds
	myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
	sd.default.samplerate = fs
	sd.default.channels = 2
	myrecording = sd.rec(int(duration * fs))
	sd.wait()

	# print(myrecording)

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

def transmit(string_array):
	print("Starting Transmission of: ",  string_array)
	playsound("1")
	time.sleep(sleeptime)
	playsound(string_array)

def errormaker(string1,string2,error1=[],error2=[]):
	string1= list(string1)
	string2= list(string2)
	for x in error1:
		string1[x-1]= str(int(not int(string1[x-1])))

	for y in error2:
		string2[y-1]= str(int(not int(string2[y-1])))
	string1= "".join(string1)
	string2= "".join(string2)

	return [string1,string2]


send_status = 0
ACKrecordtime = 4
sleeptime = 2

inp_str = ["0"]*2
inp_str[0] = sys.argv[1]
inp_str[1] = sys.argv[2]

inp_str_parity = ["0"]*2
inp_str_parity[0] = parity_maker(inp_str[0])
inp_str_parity[1] = parity_maker(inp_str[1])

print("The Parity made is: ",inp_str_parity)
inp_str_encode = sentinel(inp_str_parity)

inp_str_corrupt = errormaker(inp_str_parity[0], inp_str_parity[1], [1,3], [])
inp_str_corrupt = sentinel(inp_str_corrupt)

transmit_array = inp_str_corrupt
transmit(transmit_array)

while send_status !=1:
	print("ACK status: ", send_status)
	print("Press enter to start recording for ACK")

	temp1 = input()
	print("Now Recording")
	recording(ACKrecordtime)
	s=os.popen('bash script.sh').read()

	print("Recorded, Now Processing ...")
	if True :#s[0] == "0":	

		if s[:3] == "001":
			transmit_array = inp_str_encode
		elif s[:2] == "00":
			transmit_array = encoder(inp_str_parity[0])
		elif s[:2] == "01":
			transmit_array = encoder(inp_str_parity[1])

		print("NACK (", s, ") recieved, change ACK/NACK status or press enter to start Retransmission of parity/encode: ",  transmit_array)
		temp1=input()
		print("Your input is: ",temp1)
		if temp1 == "a":
			send_status = 1
			print ("Transmission Completed Successfully")
			break
		elif temp1 == "c01":
			transmit_array = inp_str_encode
		elif temp1 == "c0":
			transmit_array = encoder(inp_str_parity[0]) 
		elif temp1 == "c1":
			transmit_array = encoder(inp_str_parity[1])
		transmit(transmit_array)

	elif s[0] == "1":
		print("ACK recieved, change status or complete???")
		temp1=input()

		if temp1 == "c01":
			transmit_array = inp_str_encode
		elif temp1 == "c0":
			transmit_array = encoder(inp_str_parity[0]) 
		elif temp1 == "c1":
			transmit_array = encoder(inp_str_parity[1])
		changestatus(temp1)

		send_status = 1

print ("Transmission Completed Successfully")
