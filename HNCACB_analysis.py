#!/usr/bin/env python
#import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import argparse
import urllib2
from scipy.optimize import curve_fit
import re
import papua as papua
### Get the arguments

def getArgs():

        parser = argparse.ArgumentParser(description='Analyze HNcacb delay experiments')
        parser.add_argument('-files', '--file_list', help='Input Data File List')
	args = vars(parser.parse_args())

#        input_file = args['input_file']
#       output_file = args['output_file']
        return args

args = getArgs()


### Get the data for each residue in each experiment
offsets = []
delays = []
files = []
data = []
ref = [] 
with open(args['file_list']) as f:

	for row in f:
		fields = row.split()
		offsets.append(fields[0])	
		delays.append(fields[1])
		files.append(fields[2])
		
		with open(fields[2]) as f:
			aa = []
			ii = []

			for line in f:
				secs = line.split()
				if len(secs) > 3:
					aa.append((secs[0], secs[3]))

		#data.append(aa)

		if (fields[0], fields[1]) == ('-', '-'):
			ref = aa

		else:
			data.append(aa) 

systems = [i[0] for i in data[0]]
seq = []
num = []
for sys in systems:
	m = re.search('(\w)(\d+)N-H', sys)
	if m:
		seq.append(m.group(1))
		num.append(m.group(2))


#print offsets
#print delays

matrix = [[0 for x in range(len(data[:]))] for x in range(len(data[0]) )] 
#print matrix

num_spectra = len(data[:])
num_systems = len(data[0])

systems =  [x[0] for x in data[:][0]]

for i in range(0, num_spectra):
	for j in range(0, num_systems):
	#	print ref[j][0]+' '+delays[i+1], float(data[i][j][1])/float(ref[j][1])		
		matrix[j][i] = float(data[i][j][1])/float(ref[j][1])

#print matrix[0]
#print len(matrix[:])

bar_width = 0.2
index = np.arange(num_systems)
spec  = np.arange(num_spectra)
print index
loc_plts = []
colors = ['r','b','g', 'y']


for i in spec:
	dat =  [row[i] for row in matrix]
	tmp_plt = plt.bar(index+i*bar_width, dat, bar_width, color=colors[i], label=delays[i+1]+'us, '+offsets[i+1]+' ppm')
	loc_plts.append(tmp_plt)



plt.xticks(index + bar_width, [x[0] for x in systems])
plt.legend()


#dim = len(yax[0])
#w = 1.0 
#dimw = w/dim

#x = np.arange(len(yax))
#for i in range(len(yax)):
#	rects[i] = plt.bar(x, yax[i])
#	print yax[i][:]	
	

	
plt.show()
	






