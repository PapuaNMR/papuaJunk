#!/usr/bin/env python


import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as colormap
import os, sys, argparse, struct

# get the commandline options/flags

def getArgs():

        parser = argparse.ArgumentParser(description='Edits down a Bruker ser file to the FIDs listed after -fid option')
        parser.add_argument('-in', '--input_file', help='Input Data File')
	parser.add_argument('-out', '--output_file', help='Output data file')
	parser.add_argument('-lev', '--number_of_levels', help='Number of levels', default=10)
	parser.add_argument('-fac', '--factor', help='Contour factor', default=1.4)
	parser.add_argument('-base', '--base', help='Base contour', default=0)
        args = vars(parser.parse_args())

#        input_file = args['input_file']
#	output_file = args['output_file']
        return args

args = getArgs() 

header, data = papua.readnmrPipe(args['input_file'])


if args['base']:
	base = args['base']
else:
	base = np.amax(data)/15

dic = papua.fdata2dic(header)

dim = dic['FDDIMCOUNT']

#Number of points in F2 (x dimension)
xn = dic['FDSIZE']
yn = dic['FDSPECNUM']
#fdquad = dic['FDQUADFLAG']
#fdtrans = dic['FDTRANSPOSED']
#order1 = dic['FDDIMORDER1']
#print "xn = ", xn, "and yn = ", yn, "and FDQUADFLAG is ", fdquad, "and FDTRANSPOSED is ", fdtrans, "and order1 = ", order1
data2D = np.reshape(data, (yn, xn))

threshold = 0.2 * data2D.max()

peaks = papua.findPeaks(data2D, threshold, size=3, mode='wrap')

fig = plt.figure(figsize=(3,3), dpi=300)
spec = fig.add_subplot(111)
cl = float(base) * float(args['factor']) ** np.arange(int(args['number_of_levels'])) 
cmap = colormap.Blues_r
spec.contour(data2D, cl, cmap=cmap) 

for peak in peaks:
	x,y = peak.position
	spec.plot(y,x,'r.',markersize=2)


plt.tick_params(labelsize=6)
plt.show()
