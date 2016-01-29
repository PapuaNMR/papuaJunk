#!/usr/bin/env python
import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import os, sys, argparse

# get the commandline options/flags

def getArgs():

        parser = argparse.ArgumentParser(description='View a 2D schedule as matrix')
        parser.add_argument('-in', '--input_file', help='Input Data File')
        args = vars(parser.parse_args())

#        input_file = args['input_file']
#	output_file = args['output_file']
        return args



args = getArgs() 


if args['input_file']:
	file = open(args['input_file'], 'rb').readlines()
else:
	file = sys.stdin.readlines()



sched = np.zeros((len(file), 2))
i = 0
for line in file:
	array_line = line.split()
	sched[i,0] = array_line[0]	
	sched[i,1] = array_line[1]
	i += 1
xmax =  sched[:,0].max()
ymax =  sched[:,1].max()

expandedsched = np.zeros((xmax+1, ymax+1))

for line in sched:
	expandedsched[line[0], line[1]] = 1

plt.figure(figsize=(12, 9))
#ax = fig.add_subplot(1,1,1)
plt.pcolor(expandedsched, cmap = plt.cm.Greys, edgecolors='k', linewidths=1)
plt.axis([0, ymax, 0, xmax])
plt.show()

