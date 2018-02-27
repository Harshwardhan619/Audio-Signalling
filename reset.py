import os
import sounddevice as sd

def playsound(bitstring):
	for bit in bitstring:
		if bit == '1':
			os.system('paplay sounds/Networks\ 1.wav')
		else:
			os.system('paplay sounds/Networks\ 2.wav')

playsound("10101")