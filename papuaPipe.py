import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import os, sys, argparse

# get the commandline options/flags

def getArgs():

        parser = argparse.ArgumentParser(description='Edits down a Bruker ser file to the FIDs listed after -fid option')
        parser.add_argument('-in', '--input_file', help='Input Data File')
	parser.add_argument('-out', '--output_file', help='Output data file')
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


data = np.frombuffer(file, dtype='float32', count=(length-512), offset=513)

dic = papua.fdata2dic(header)

dim = dic['FDDIMCOUNT']

#Number of points in F2 (x dimension)
xn = dic['FDSIZE']
yn = dic['FDSPECNUM']
fdquad = dic['FDQUADFLAG']
fdtrans = dic['FDTRANSPOSED']
order1 = dic['FDDIMORDER1']
print "xn = ", xn, "and yn = ", yn, "and FDQUADFLAG is ", fdquad, "and FDTRANSPOSED is ", fdtrans, "and order1 = ", order1
