#!/usr/bin/env python
import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import argparse
import urllib2
from scipy.optimize import curve_fit
import re

### Get the arguments

def getArgs():

        parser = argparse.ArgumentParser(description='Grab CaCa-1 Matches and test them for accuracy on peak shape')
        parser.add_argument('-data', '--data_file', help='Input HNCA Data File')
	parser.add_argument('-shifts', '--shifts_file', help='Input shifts file (sparky shift file)')
	parser.add_argument('-seq', '--sequence_file', help='Sequence file (one letter on one line)')
	parser.add_argument('-criterion', '--Hz_criterion', help='seperation required forthere to beno overlap (in Hz)')
	args = vars(parser.parse_args())

#        input_file = args['input_file']
#       output_file = args['output_file']
        return args

args = getArgs()

# read shift file

Seq = []
CA = []
CAcoord = []
CAm1 = []
CAm1coord = []

with open(args['shifts_file']) as f:
        for row in f:
                Data = row.split()
                if len(Data) == 7 and Data[0][0] != '#':
                        num = int(re.findall("[-+]?\d+[\.]?\d*", Data[0])[0])
                        if Data[0].find('-N-H') != -1: # CA shifts
		       		CA.append([num, float(Data[4])])
				CAcoord.append([num, float(Data[1]), float(Data[2]), float(Data[3])])
			        Seq.append(Data[0][0])
                        else: # CA-1 shifts
                                CAm1.append([num, float(Data[4])])
				CAm1coord.append([num, float(Data[1]), float(Data[2]), float(Data[3])])

# read sequence file
with open(args['sequence_file']) as f:
	input_sequence = "".join(line.rstrip() for line in f)  
	input_sequence = list(input_sequence.replace(" ", ""))


# figure out residue matching

res = []
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
                                         diffs.append([CAm1shift[0], diff])
                        res.append([residue, CAshift[0], diffs])
                        if len(diffs) > maxdiffs:
                                maxdiffs = len(diffs)
        if flag == 0:
                res.append([residue, i, 'no assignment']) 
print res 
#print CAcoord
for entry in res:
	diff_list = entry[2]
	if len(diff_list) != 0 and diff_list != 'no assignment':
		min_value = min(x[1] for x in diff_list)
#		closest = [x for x in diff_list if x[1] == min_value]
#		if entry[1] != closest[0][0]:
#			print entry[1], closest[0][0]
#		print entry[1],  [[x[0], x[1]] for x in diff_list]

#print CAcoord
#print CAm1coord

### Get the NMR spectrum 

header, data = papua.readnmrPipe(args['data_file'])

dic = papua.fdata2dic(header)
xn = dic['FDSIZE']
yn = dic['FDSPECNUM']
zn = dic['FDF3SIZE']

data3D = np.reshape(data, (zn, yn, xn)) # data is in 1HN, 13Ca, 15NH order

xsw_hz = dic['FDF2SW'] #H
ysw_hz = dic['FDF3SW'] #C
zsw_hz = dic['FDF1SW'] #N

xobs_mhz = dic['FDF2OBS']
yobs_mhz = dic['FDF3OBS']
zobs_mhz = dic['FDF1OBS']

xcar_ppm = dic['FDF2CAR']
ycar_ppm = dic['FDF3CAR']
zcar_ppm = dic['FDF1CAR']

xsw_ppm = ((dic['FDF2FTSIZE']/xn)*(dic['FDF2SW']/dic['FDF2OBS']))
ysw_ppm = dic['FDF3SW']/dic['FDF3OBS']
zsw_ppm = dic['FDF1SW']/dic['FDF1OBS']


print xsw_ppm, xcar_ppm, ysw_ppm, ycar_ppm, zsw_ppm, zcar_ppm

for system in res:
	if system[2] != 'no assignment' and len(system[2]) > 1:
		for CA in CAcoord:
			if CA[0] == system[1]:
				print CA[0], 'CA:', CA[1], CA[2], CA[3]
				CA_x_shift_ppm, CA_y_shift_ppm, CA_z_shift_ppm = CA[3], CA[1], CA[2]
				CA_x_right_ppm = xcar_ppm + 0.5*xsw_ppm
				x_point = round((1.0-((CA_x_shift_ppm - xcar_ppm)/(CA_x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)
				y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - CA_y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)
				z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - CA_z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)

				bestCoord = [z_point, x_point]
				maxCa = 0
				for i in [x_point-2, x_point-1, x_point, x_point+1, x_point+2]:
					for j in [z_point-2, z_point-1, z_point, z_point+1, z_point+2]:
						CaLine = data3D[j,(y_point-14):(y_point+15),i]
						if CaLine.max() > maxCa:
							maxCa = CaLine.max()
							bestCoord = [j, i]
				z_point, x_point = bestCoord
				maxy_point = data3D[z_point, (y_point-14):(y_point+15), x_point].argmax()
				y_point = y_point+maxy_point-14
				[CA_x_point, CA_y_point, CA_z_point] = [x_point, y_point, z_point]
				CApeak = data3D[CA_z_point,(CA_y_point-14):(CA_y_point+15),CA_x_point]
				CAmax = max(CApeak)
				x = np.arange(29.0)
				plt.plot(x,CApeak, linewidth=5.0)

		l2norm = [0,100000000000000000000,0]
		for match in system[2]:
			for CAm1 in CAm1coord:
				if CAm1[0] == match[0]:
					#print '\t', CAm1[0], 'CA-1:', CAm1[1], CAm1[2], CAm1[3]
					CAm1_x_shift_ppm, CAm1_y_shift_ppm, CAm1_z_shift_ppm = CAm1[3], CAm1[1], CAm1[2]
					CAm1_x_right_ppm = xcar_ppm + 0.5*xsw_ppm
					x_point = round((1.0-((CAm1_x_shift_ppm - xcar_ppm)/(CAm1_x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)
					y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - CAm1_y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)
					z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - CAm1_z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)
					bestCoord = [z_point, x_point]
					maxCa = 0
					
					
					for fiddle in np.arange(-1,2):
						#print y_point 
						y_point_f = y_point + fiddle	
						#print y_point_f
						for i in [x_point-2, x_point-1, x_point, x_point+1, x_point+2]:
							for j in [z_point-2, z_point-1, z_point, z_point+1, z_point+2]:
								CaLine = data3D[j,(y_point_f-14):(y_point_f+15),i]
								if CaLine.max() > maxCa:
									maxCa = CaLine.max()
									bestCoord = [j, i]
						z_point, x_point = bestCoord
						maxy_point = data3D[z_point, (y_point_f-14):(y_point_f+15), x_point].argmax()
						y_point_f = y_point_f+maxy_point-14+fiddle
						[CAm1_x_point, CAm1_y_point, CAm1_z_point] = [x_point, y_point_f, z_point]
						CAm1peak = data3D[CAm1_z_point,(CAm1_y_point-14):(CAm1_y_point+15),CAm1_x_point]
						CAm1max = max(CAm1peak)
						CAm1peak = CAm1peak * (CAmax/CAm1max)
						x = np.arange(29.0)
						if fiddle == 0:
							plt.plot(x,CAm1peak, linewidth=2.0)
						if (CApeak - CAm1peak).std() < l2norm[1]:
							l2norm[1] = (CApeak - CAm1peak).std()
							l2norm[0] = CAm1[0]
							l2norm[2] = fiddle
		print l2norm	
	
	plt.show()


#for CA in CAcoord:
#	for CAm1 in CAm1coord:
#		if CA[0] == CAm1[0] : # its a match!
#			CA_x_shift_ppm, CA_y_shift_ppm, CA_z_shift_ppm = CA[3], CA[1], CA[2]
#			CA_x_right_ppm = xcar_ppm + 0.5*xsw_ppm
#			x_point = round((1.0-((CA_x_shift_ppm - xcar_ppm)/(CA_x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)
#			y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - CA_y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)
#			z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - CA_z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)
#			bestCoord = [z_point, x_point]
#			maxCa = 0
#		        for i in [x_point-2, x_point-1, x_point, x_point+1, x_point+2]:
#				for j in [z_point-2, z_point-1, z_point, z_point+1, z_point+2]:
#					CaLine = data3D[j,(y_point-14):(y_point+15),i]
#					if CaLine.max() > maxCa:
#						maxCa = CaLine.max()
#		                                bestCoord = [j, i]
#			z_point, x_point = bestCoord
#			maxy_point = data3D[z_point, (y_point-14):(y_point+15), x_point].argmax()
#			y_point = y_point+maxy_point-14
#			[CA_x_point, CA_y_point, CA_z_point] = [x_point, y_point, z_point]
#			CApeak = data3D[CA_z_point,(CA_y_point-14):(CA_y_point+15),CA_x_point]
#			x = np.arange(29.0)
#			plt.plot(x,CApeak, linewidth=5.0)
#
#			CAm1_x_shift_ppm, CAm1_y_shift_ppm, CAm1_z_shift_ppm = CAm1[3], CAm1[1], CAm1[2]
#			CAm1_x_right_ppm = xcar_ppm + 0.5*xsw_ppm
#			x_point = round((1.0-((CAm1_x_shift_ppm - xcar_ppm)/(CAm1_x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)
#			y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - CAm1_y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)
#			z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - CAm1_z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)
#			bestCoord = [z_point, x_point]
#			maxCa = 0
#			for i in [x_point-2, x_point-1, x_point, x_point+1, x_point+2]:
#				for j in [z_point-2, z_point-1, z_point, z_point+1, z_point+2]:
#					CaLine = data3D[j,(y_point-14):(y_point+15),i]
#					if CaLine.max() > maxCa:
#						maxCa = CaLine.max()
#						bestCoord = [j, i]
#			z_point, x_point = bestCoord
#			maxy_point = data3D[z_point, (y_point-14):(y_point+15), x_point].argmax()
#			y_point = y_point+maxy_point-14
#			[CAm1_x_point, CAm1_y_point, CAm1_z_point] = [x_point, y_point, z_point]
#			
#			CAm1peak = data3D[CAm1_z_point,(CAm1_y_point-14):(CAm1_y_point+15),CAm1_x_point]
#			
#			CAm1max = max(CAm1peak)
#			CAmax = max(CApeak)
#			CAm1peak = CAm1peak * (CAmax/CAm1max)
#
#			x = np.arange(29.0)
#			plt.plot(x,CAm1peak, linewidth=5.0)
#
#
#	plt.show()
#
