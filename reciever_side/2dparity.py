import numpy as np

# m= int(input(),10)
# n= int(input(),10)
# size=m*n
def paritydecoder(string):
	
	string1= string[:-9]
	string2= string1

	length=len(string1)
	xtralength= 20-length
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
		print("error is corrected",row*5+column+1)
		return ''.join([str(i) for i in array])[:-xtralength]
		
	if row_faults>0 or column_faults>0:
		print("error has occurred" +" "+ string1[:-xtralength])
		return -1
	else:
		return 0
	# print(row,column)

print(paritydecoder("00000001111001100001101"))