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

if args['input_file']:
#	file = open(args['input_file'], 'rb').read()
	data = np.fromfile(args['input_file'], 'float32')
else:
	stdin = sys.stdin.read()
	data = np.frombuffer(stdin, dtype=np.float32)

#length = len(file)/4

#`data = np.fromfile(args['input_file'], 'float32')
if data[2] - 2.345 > 1e-6:  # check for byteswap
    data = data.byteswap()

header = data[:512]
data =  data[512:]
if args['base']:
	base = args['base']
else:
	base = np.amax(data)/15

dic = papua.fdata2dic(header)

dim = dic['FDDIMCOUNT']

#Number of points in F2 (x dimension)
xn = dic['FDSIZE']
yn = dic['FDSPECNUM']
fdquad = dic['FDQUADFLAG']
fdtrans = dic['FDTRANSPOSED']
order1 = dic['FDDIMORDER1']
#print "xn = ", xn, "and yn = ", yn, "and FDQUADFLAG is ", fdquad, "and FDTRANSPOSED is ", fdtrans, "and order1 = ", order1
#print data.shape
data2D = np.reshape(data, (yn, xn))
fig = plt.figure(figsize=(3,3), dpi=300)
spec = fig.add_subplot(111)
cl = float(base) * float(args['factor']) ** np.arange(int(args['number_of_levels'])) 
#print cl
cmap = colormap.Blues_r
spec.contour(data2D, cl, cmap=cmap) 
#plt.xticks(fontsize = 5)
#plt.yticks(fontsize = 5)
plt.tick_params(labelsize=6)
plt.show()

#n, bins, patches = plt.hist(data, bins=range(-10,100000000, 100000))
#plt.show()
