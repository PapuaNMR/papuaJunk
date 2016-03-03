#!/usr/bin/env python
import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.optimize import curve_fit

def getArgs():

        parser = argparse.ArgumentParser(description='Fit Ca peaks to Pyruvate three-peak model')
        parser.add_argument('-in', '--input_file', help='Input Data File')
        args = vars(parser.parse_args())

#        input_file = args['input_file']
#       output_file = args['output_file']
        return args

args = getArgs()

header, data = papua.readnmrPipe(args['input_file'])

dic = papua.fdata2dic(header)
xn = dic['FDSIZE']
yn = dic['FDSPECNUM']
zn = dic['FDF3SIZE']

data3D = np.reshape(data, (zn, yn, xn))

Ca = data3D[154,:,305]



def pyruvate_func(x, k13, k2, s13, s2, m1, d):
	
	first_peak = (k13)*np.exp((-((x-m1-d)**2))/(2*(s13**2)))
	second_peak = (k2)*np.exp((-((x-m1)**2))/(2*(s2**2)))
	third_peak = (k13)*np.exp((-((x-m1+d)**2))/(2*(s13**2)))

	return first_peak + second_peak + third_peak




ymeasure = Ca[(1008-13):(1008+14)]

x = np.arange(27.0)
max = ymeasure.max()
params = curve_fit(pyruvate_func, x, ymeasure, p0=([0.5*max, max, 5, 5, 13.5, 10]))

p = params[0]
print p




xpredict = np.arange(0, 27.0, 0.01)


ypredict = pyruvate_func(xpredict, p[0], p[1], p[2], p[3], p[4], p[5])


plt.plot(x,ymeasure, linewidth=5.0)
plt.plot(xpredict, ypredict, linewidth=5.0)

#plt.plot(Ca)

plt.show()
