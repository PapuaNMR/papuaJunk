#!/usr/bin/env python

import os
import argparse
import re
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
def getArgs():
	parser = argparse.ArgumentParser(description='COmpare CA and CA-1 for overlaps over entire list')
	parser.add_argument('-file', '--shift_file', help='Sparky list of CA and CA-1 shifts with shifts in Hz')
	parser.add_argument('-criterion', '--Hz_criterion', help='seperation required forthere to beno overlap (in Hz)')
	parser.add_argument('-seq', '--sequence_file', help='Single Letter list of Amino Acids all on one line')

	args = vars(parser.parse_args())

	return args
		     


args = getArgs()
Seq = []
CA = []
CAm1 = []

print args['Hz_criterion']

# read sequence file
with open(args['sequence_file']) as f:
	        input_sequence = "".join(line.rstrip() for line in f)  

		input_sequence = list(input_sequence.replace(" ", ""))

# read shift file
with open(args['shift_file']) as f:
	for row in f:
		Data = row.split()
		if len(Data) == 7 and Data[0][0] != '#':
			num = int(re.findall("[-+]?\d+[\.]?\d*", Data[0])[0])
			
			if Data[0].find('-N-H') != -1: # CA shifts
				CA.append([num, float(Data[4])])
				Seq.append(Data[0][0])

			else: # CA-1 shifts
				CAm1.append([num, float(Data[4])])


res = []
#for CAshift in CA:
#	thisdata = [input_sequence[CAshift[0]-1], CAshift[0]]
#	for CAm1shift in CAm1:
#		diff = abs(CAshift[1] - CAm1shift[1])
#		if diff < float(args['Hz_criterion']):
#			thisdata.append(diff)
#	res.append(thisdata)

i = 0
maxdiffs = 0
for residue in input_sequence:
	i += 1
	diffs=[]
	flag = 0
	for CAshift in CA:
		if CAshift[0] == i:
			flag = 1
			for CAm1shift in CAm1:
				diff = abs(CAshift[1] - CAm1shift[1])
				if diff < float(args['Hz_criterion']):
					 diffs.append(diff)
			res.append([residue, CAshift[0], diffs])
			if len(diffs) > maxdiffs:
				maxdiffs = len(diffs)
	if flag == 0:
		res.append([residue, i])
print res



tot = 0
list = []

for data in res:
	if len(data) > 2:
		num = len(data[2])
		list.append(num)


print np.mean(list)
print np.std(list)

canvas = canvas.Canvas("assignable.pdf", pagesize=letter)
#canvas.setFont('Courier-Bold', 20)
#canvas.drawString(25,750,"ABCDEFGHIJ ABCDEFGHIJ ABCDEFGHIJ ABCDEFGHIJ")
textobject = canvas.beginText()
textobject.setTextOrigin(0.5*inch, 10*inch)
textobject.setFont("Courier-Bold", 20)
c = 1 
r = 1 
print maxdiffs
maxdiffs=20

for data in res:
	aa = data[0]
	if len(data) == 3:
		score = float(len(data[2]))/float(maxdiffs)
		if score > 0.5:
			Rscore = 1.0
			Gscore = score/2.0 - 0.5
		else:
			Gscore = 1.0
			Rscore = score/2.0 - 0.5
		Rscore = 1.0
		Gscore = 1.0 - score


		if len(data[2]) == 1:
			textobject.setFont("Courier-Bold", 20)

		textobject.setFillColorRGB(Rscore,Gscore,0.0)
		textobject.setStrokeColorRGB(0,0,0)
		textobject.setTextRenderMode(2)
		canvas.setLineWidth(0.5)
		if len(data[2]) == 1:
			textobject.setFillColorRGB(0,1.0,0)

	else:
		textobject.setFillColorRGB(0.0,0.0,0.0)
	#canvas.setFillColorRGB(0.2,0.5,0.0)
	if c % 10 == 0 and c % 40 != 0:
		textobject.textOut(aa+' ')
	elif (c % 40 == 0):
		textobject.textLine(aa)
	else:
		textobject.textOut(aa)
	c += 1
	#print aa
canvas.drawText(textobject)


canvas.save()
os.system('open assignable.pdf')

matches = []
min = 1
max = 1
for data in res:
	if len(data) == 3:
		matches.append(len(data[2]))
		if len(data[2]) < min:
			min = len(data[2])
		if len(data[2]) > max:
			max = len(data[2])
print matches
print min
print max

bins = range(max+5)
n, bins, patches = plt.hist(matches, bins, normed=0, histtype='bar', rwidth=0.8)

plt.show()
