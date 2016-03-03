#!/usr/bin/env python
import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.optimize import curve_fit


### Get the arguments

def getArgs():

        parser = argparse.ArgumentParser(description='Fit Ca peaks to Pyruvate three-peak model')
        parser.add_argument('-data', '--data_file', help='Input Data File')
	parser.add_argument('-shifts', '--shifts_file', help='Input shifts file (csv file)')
        args = vars(parser.parse_args())

#        input_file = args['input_file']
#       output_file = args['output_file']
        return args

args = getArgs()


### Get the shifts we need (H, N, CA) for each residue

shifts_ppm = []
i = 0
with open(args['shifts_file']) as f:
	for row in f:
		Data = row.split(';')
		if Data[0] and  Data[1] and Data[3] and Data[4]:
			shifts_ppm.append([Data[0], Data[1], Data[4], Data[3]]) # H C N order

#print shifts_ppm



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

#print xsw_hz, ysw_hz, zsw_hz

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

x_shift = 8.33
y_shift = 57.54
z_shift = 121.68

xdiff = x_shift - xcar_ppm
ydiff = y_shift - ycar_ppm
zdiff = z_shift - zcar_ppm

print xdiff, ydiff, zdiff

#print dic['FDF2LABEL']    
#print dic['FDF2APOD']      
#print dic['FDF2SW']        
#print dic['FDF2OBS']       
#print dic['FDF2ORIG']      
#print dic['FDF2UNITS']     
#print dic['FDF2QUADFLAG']  
#print dic['FDF2FTFLAG']    
#print dic['FDF2AQSIGN']    
#print dic['FDF2LB']        
#print dic['FDF2CAR']       
#print dic['FDF2CENTER']    
#print dic['FDF2OFFPPM']    
#print dic['FDF2P0']        
#print dic['FDF2P1']        
#print dic['FDF2APODCODE']  
#print dic['FDF2APODQ1']    
#print dic['FDF2APODQ2']    
#print dic['FDF2APODQ3']    
#print dic['FDF2C1']        
#print dic['FDF2ZF']        
#print dic['FDF2X1']        
#print dic['FDF2XN']        
#print dic['FDF2FTSIZE']    
#print dic['FDF2TDSIZE']    





Ca = data3D[162,:,429]



def pyruvate_func(x, k13, k2, s13, s2, m1, d):
	
	first_peak = (k13)*np.exp((-((x-m1-d)**2))/(2*(s13**2)))
	second_peak = (k2)*np.exp((-((x-m1)**2))/(2*(s2**2)))
	third_peak = (k13)*np.exp((-((x-m1+d)**2))/(2*(s13**2)))

	return first_peak + second_peak + third_peak




ymeasure = Ca[(785-13):(785+14)]

x = np.arange(27.0)
max = ymeasure.max()
params = curve_fit(pyruvate_func, x, ymeasure, 
		p0=([0.1*max, max, 5, 5, 13.5, 4.3]),
		bounds=([0.001*max, 0.5*max, 1, 1, 10, 3.7],[max, 2*max, 10, 10, 17, 4.9]),
		method='dogbox'
		)

p = params[0]
print p




xpredict = np.arange(0, 27.0, 0.01)


ypredict = pyruvate_func(xpredict, p[0], p[1], p[2], p[3], p[4], p[5])


plt.plot(x,ymeasure, linewidth=5.0)
plt.plot(xpredict, ypredict, linewidth=5.0)

#plt.plot(Ca)

plt.show()
