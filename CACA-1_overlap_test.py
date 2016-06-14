#!/usr/bin/env python

import argparse
import re
import numpy as np

def getArgs():
	parser = argparse.ArgumentParser(description='COmpare CA and CA-1 for overlaps over entire list')
	parser.add_argument('-file', '--shift_file', help='Sparky list of CA and CA-1 shifts with shifts in Hz')
	parser.add_argument('-criterion', '--Hz_criterion', help='seperation required forthere to beno overlap (in Hz)')

	args = vars(parser.parse_args())

	return args
		     


args = getArgs()
CA = []
CAm1 = []
with open(args['shift_file']) as f:
	for row in f:
		Data = row.split()
		if len(Data) == 7 and Data[0][0] != '#':
			num = int(re.findall("[-+]?\d+[\.]?\d*", Data[0])[0])
			if Data[0].find('-N-H') != -1: # CA shifts
				CA.append([num, float(Data[4])])

			else: # CA-1 shifts

				CAm1.append([num, float(Data[4])])


#print CA
#print CAm1

res = []
for CAshift in CA:
	thisdata = [CAshift[0]]
	for CAm1shift in CAm1:
		diff = abs(CAshift[1] - CAm1shift[1])
		if diff < float(args['Hz_criterion']):
			thisdata.append(diff)
	res.append(thisdata)

i = 0
tot = 0
list = []

for data in res:
	i += 1
	tot = tot + len(data)-1
	num = len(data)-1
	list.append(num)



print np.mean(list)
print np.std(list)
