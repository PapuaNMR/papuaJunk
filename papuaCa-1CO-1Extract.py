#!/usr/bin/env python
import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import argparse
import urllib2
from scipy.optimize import curve_fit


### Get the arguments

def getArgs():

        parser = argparse.ArgumentParser(description='Fit Ca peaks to Pyruvate three-peak model')
        parser.add_argument('-HNCA', '--data_file_HNCA', help='Input Data File HNCA')
	parser.add_argument('-HNCO', '--data_file_HNCO', help='Input Data File HNCO')
	parser.add_argument('-shifts', '--shifts_file', help='Input shifts file (csv file)')
	parser.add_argument('-seq', '--sequence_file', help='Sequence file (one letter, new line)')
	args = vars(parser.parse_args())

#        input_file = args['input_file']
#       output_file = args['output_file']
        return args

args = getArgs()


### Get the shifts we need (H, N, CA) for each residue

shifts_CA_ppm = []
shifts_CO_ppm = []
i = 0
with open(args['shifts_file']) as f:
	for row in f:
		Data = row.split(';')
		if len(Data) == 5 and Data[0] and  Data[1] and Data[3] and Data[2] and Data[0][0] != '#':
			shifts_CA_ppm.append([Data[0], Data[1], Data[3], Data[2]]) # H CA-1 N order
			shifts_CO_ppm.append([Data[0], Data[1], Data[4], Data[2]]) # H CO-1 N order

### Get sequence and create dictionary with entry for each amino acid

spectra_amino_dic = {}
sequence = []
with open(args['sequence_file']) as f:
	for row in f:
		if row not in spectra_amino_dic:
			spectra_amino_dic[row[:-1]] = []	
		sequence.append(row[:-1])	





#print spectra_amino_dic
#print sequence


### Get the NMR spectrum 

header, data = papua.readnmrPipe(args['data_file_HNCA'])

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



#x_shift_ppm = 8.328
#y_shift_ppm = 57.536
#z_shift_ppm = 121.634
line_num = 0
while line_num < len(shifts_CA_ppm):

	x_shift_ppm, y_shift_ppm, z_shift_ppm = float(shifts_CA_ppm[line_num][1]), float(shifts_CA_ppm[line_num][2]), float(shifts_CA_ppm[line_num][3])
	x_right_ppm = xcar_ppm + 0.5*xsw_ppm
	x_point = round((1.0-((x_shift_ppm - xcar_ppm)/(x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)
	y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)
	z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)
	bestCoord = [z_point, x_point]

	maxCa = 0

	for i in [x_point-3, x_point-2, x_point-1, x_point, x_point+1, x_point+2, x_point+3]:
		for j in [z_point-3, z_point-2, z_point-1, z_point, z_point+1, z_point+2, z_point+3]:
			Ca = data3D[j,(y_point-15):(y_point+16),i]
			if Ca.max() > maxCa:
				maxCa = Ca.max()
				bestCoord = [j, i]

	z_point, x_point = bestCoord

	Ca = data3D[z_point,(y_point-16):(y_point+17),x_point]

	CA = ['{:f}'.format(item) for item in Ca]

	print sequence[int(shifts_CA_ppm[line_num][0])-1]+',', str(int(shifts_CA_ppm[line_num][0]))+',', ', '.join(map(str, CA)) 

	plt.plot(Ca.tolist())
	plt.show()

	line_num += 1

#line_num = 0
#while line_num < len(shifts_ppm):

#        x_shift_ppm, y_shift_ppm, z_shift_ppm = float(shifts_m1_ppm[line_num][1]), float(shifts_m1_ppm[line_num][2]), float(shifts_m1_ppm[line_num][3])
#        x_right_ppm = xcar_ppm + 0.5*xsw_ppm
#        x_point = round((1.0-((x_shift_ppm - xcar_ppm)/(x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)
#        y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)
#        z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)
#        bestCoord = [z_point, x_point]

#        maxCa = 0

#        for i in [x_point-2, x_point-1, x_point, x_point+1, x_point+2]:
#                for j in [z_point-2, z_point-1, z_point, z_point+1, z_point+2]:
#                        Ca = data3D[j,(y_point-15):(y_point+16),i]
#                        if Ca.max() > maxCa:
#                                maxCa = Ca.max()
#                                bestCoord = [j, i]

#        z_point, x_point = bestCoord

#        Ca = data3D[z_point,(y_point-16):(y_point+17),x_point]

#	CA = ['{:f}'.format(item) for item in Ca]

#        print sequence[int(shifts_m1_ppm[line_num][0])-1]+',', str(int(shifts_m1_ppm[line_num][0]))+'-1,', ', '.join(map(str, CA)) 

#        plt.plot(Ca.tolist())
#        plt.show()


        #line_num += 1

