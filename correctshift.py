#!/usr/bin/env python

import argparse
import re

def getArgs():
	parser = argparse.ArgumentParser(description='Apply correct to tripe rez Sparky peak file')
	parser.add_argument('-shifts', '--shift_file', help='Sparky list of CA N H shifts in ppm')

	args = vars(parser.parse_args())

	return args
		     


args = getArgs()
CA = []
CAm1 = []
with open(args['shift_file']) as f:
	for row in f:
		Data = row.split()
		if len(Data) == 7 and Data[0][0] != '#':
			print Data[0], "\t", float(Data[1])+0.022, "\t", float(Data[2])+0.137, "\t", float(Data[3])+0.005

