#!/usr/bin/env python
#import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import argparse
import urllib2
from scipy.optimize import curve_fit


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
data = {}
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

		if (fields[0], fields[1]) == ('-', '-'):
			ref = aa

		else:
			data[(fields[0], fields[1])] = aa


print data



#i = 0
#compile = {} 
#for i in range(0, len(ref)):
#	line = []
#	for spectrum in data:
#		line.append(float(data[spectrum][i][1])/float(ref[i][1]))
#		#print data[spectrum][i][0], spectrum, float(data[spectrum][i][1])/float(ref[i][1])
#	compile[data[spectrum][i][0]] = line

#num_spectra = 

#print compile








#cat = [] 
#yax = () 
#for key in compile:
#	cat.append(key)
#	residue = ()
#	for i in range(0, len(compile[key])):
#		residue = residue + (compile[key][i],)
#	yax = yax + (residue,)

#print yax

#dim = len(yax[0])
#w = 1.0 
#dimw = w/dim

#x = np.arange(len(yax))
#for i in range(len(yax)):
#	rects[i] = plt.bar(x, yax[i])
#	print yax[i][:]	
	

	
plt.show()
	






