import numpy as np
def parity_maker(string):
	length=len(string)
	if length <20:
		str1= string+ '0'*(20-length)
	array= [int(i) for i in list(str1)]
	mat= np.matrix(array)
	mat.resize(4,5)
	row_sums= mat.sum(axis=1)
	column_sums= mat.sum(axis=0)
	for i in range(4):
		string= string+ str(row_sums.item(i)%2)

	for i in range(5):
		string= string+ str(column_sums.item(i)%2)

	return string

print(parity_maker("10000011111001"))