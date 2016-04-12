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


#print seq[34], num[34], matrix[34]

fig = plt.figure()
ax = fig.add_subplot(111)
box = ax.get_position()



spec = np.arange(num_spectra)
bar_width = 0.2
colours = ['r','b','g', 'y']
for key in papua.aa_dic:
	group_by_aa = []
	for i in range(num_systems):
		index = 0 # 
		#ax.cla()
		if seq[i] == key:
			#print seq[i], num[i], matrix[i]
			group_by_aa.append([seq[i], num[i], matrix[i]])

	dat = [x[2] for x in group_by_aa[:]]
	aa = [x[0]+x[1] for x in group_by_aa[:]]
	
	if len(aa) > 0:
		index = np.arange(len(aa))
		ax.cla()
		loc_plts = []
		for j in spec:
			da = [row[j] for row in dat]
			tmp_plt = plt.bar(index+j*bar_width, da, bar_width, color=colours[j], label=delays[j+1]+'us, '+offsets[j+1]+' ppm')
			loc_plts.append(tmp_plt)

		plt.xticks(index + 2*bar_width, aa)
		ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
		plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))	
		fig.savefig("plots/"+key+".pdf")

