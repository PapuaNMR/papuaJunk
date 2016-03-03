#!/usr/bin/env python
#import papua as papua
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


def pyruvate_func(x, k13, k2, s13, s2, m1, d):
#	first_peak = (k1/s)*np.exp((-((x-m1)**2))/(2*(s**2)))
#	second_peak = (k2/s)*np.exp((-((x-m2)**2))/(2*(s**2)))
#	third_peak = (k3/s)*np.exp((-((x-m3)**2))/(2*(s**2)))

	first_peak = (k13)*np.exp((-((x-m1-d)**2))/(2*(s13**2)))
	second_peak = (k2)*np.exp((-((x-m1)**2))/(2*(s2**2)))
	third_peak = (k13)*np.exp((-((x-m1+d)**2))/(2*(s13**2)))


	return first_peak + second_peak + third_peak


ymeasure = np.array([-2404110.25000, 1407502.87500, 2055887.75000, 2479897.50000, 1648007.62500, 2328414.50000,-3384462.50000, 3807001.75000, 2728063.50000, 1609838.25000,-3020459.00000,-2565403.50000, 5429776.50000, 10353173.00000, 10584025.00000, 10531778.00000, 20147162.00000, 40511148.00000, 64238360.00000, 87567056.00000, 118140576.00000, 181521504.00000, 285248416.00000, 362164384.00000, 324987296.00000, 197501904.00000, 92006800.00000, 60131764.00000, 61869652.00000, 53806068.00000, 31604644.00000, 10003786.00000, 2514109.25000, 6383070.50000, 7441508.00000, 1941307.00000,-4313932.50000,-3355982.50000,-1699352.12500,-2052967.87500,-1944998.87500, 2082903.87500, 2746743.75000, 2138383.25000, 2067050.50000,-3102726.00000,-2630110.75000])

#ymeasure = np.array([-9479552.00000,-4830927.50000,-2648416.75000,-4564425.50000,-4808560.00000,-4413367.50000,-7302069.50000,-13373112.00000,-12818494.00000,-5524100.00000,8175881.50000,22911592.00000,45246636.00000,63502692.00000,68905768.00000,80913288.00000,128582080.00000,209280080.00000,297325728.00000,341618464.00000,305735712.00000,287061792.00000,409812928.00000,610178432.00000,667685376.00000,506181888.00000,291122144.00000,191029872.00000,202621488.00000,225991680.00000,196307392.00000,127446272.00000,68427760.00000,40777184.00000,31211356.00000,24656236.00000,18197344.00000,14506482.00000,14894635.00000,15040497.00000,10582719.00000,4098529.00000,3147637.00000,3731190.00000,7546011.00000,9563360.00000,6626809.00000])


x = np.arange(47.0)
max = ymeasure.max()
params = curve_fit(pyruvate_func, x, ymeasure, p0=([0.5*max, max, 5, 5, 23.5, 10]))

p = params[0]
print p



#k13 =100
#k2 = 150
#s = 1.5 
#m1 = 5.7
#m2 = 10.7
#m3 = 15.7 

#y = pyruvate_func(x, k13, k2, s, m1, m2, m3)

xpredict = np.arange(0, 47.0, 0.01)


ypredict = pyruvate_func(xpredict, p[0], p[1], p[2], p[3], p[4], p[5])


plt.plot(x,ymeasure, linewidth=5.0)
plt.plot(xpredict, ypredict, linewidth=5.0)
plt.show()
