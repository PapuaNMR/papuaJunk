#!/usr/bin/env python
import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as colormap
import os, sys, argparse

# get the commandline options/flags

def getArgs():

        parser = argparse.ArgumentParser(description='Edits down a Bruker ser file to the FIDs listed after -fid option')
        parser.add_argument('-in', '--input_file', help='Input Data File')
	parser.add_argument('-out', '--output_file', help='Output data file')
	parser.add_argument('-lev', '--number_of_levels', help='Number of levels', default=20)
	parser.add_argument('-fac', '--factor', help='Contour factor', default=1.4)
	parser.add_argument('-base', '--base', help='Base contour', default=0)
        args = vars(parser.parse_args())

#        input_file = args['input_file']
#	output_file = args['output_file']
        return args



args = getArgs() 


if args['input_file']:
	file = open(args['input_file'], 'rb').read()
else:
	file = sys.stdin.read()

length = len(file)/4

header = np.frombuffer(file, 'float32', 512)
if header[2] - 2.345 > 1e-6:
	header = header.byteswap()

data = np.fromfile(args['input_file'], 'float32')
if data[2] - 2.345 > 1e-6:  # check for byteswap
    data = data.byteswap()

data =  data[512:]
print data


#data = np.frombuffer(file, dtype='float32', count=(length-512), offset=513)

dic = papua.fdata2dic(header)

dim = dic['FDDIMCOUNT']

#Number of points in F2 (x dimension)
xn = dic['FDSIZE']
yn = dic['FDSPECNUM']
fdquad = dic['FDQUADFLAG']
fdtrans = dic['FDTRANSPOSED']
order1 = dic['FDDIMORDER1']
print "xn = ", xn, "and yn = ", yn, "and FDQUADFLAG is ", fdquad, "and FDTRANSPOSED is ", fdtrans, "and order1 = ", order1
print data.shape
data2D = np.reshape(data, (yn, xn))


#print data2D.shape
print data2D[21,101]

fig = plt.figure()
spec = fig.add_subplot(111)
cl = float(args['base']) * float(args['factor']) ** np.arange(int(args['number_of_levels'])) 
print cl
cmap = colormap.Blues_r
spec.contour(data2D, cl, cmap=cmap) 
plt.show()
