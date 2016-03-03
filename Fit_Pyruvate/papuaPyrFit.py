#!/usr/bin/env python
#import papua as papua
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.optimize import curve_fit



def pyruvate_func(x, k13, k2, s, m1, d):
#	first_peak = (k1/s)*np.exp((-((x-m1)**2))/(2*(s**2)))
#	second_peak = (k2/s)*np.exp((-((x-m2)**2))/(2*(s**2)))
#	third_peak = (k3/s)*np.exp((-((x-m3)**2))/(2*(s**2)))

	first_peak = (k13)*np.exp((-((x-m1-d)**2))/(2*(s**2)))
	second_peak = (k2)*np.exp((-((x-m1)**2))/(2*(s**2)))
	third_peak = (k13)*np.exp((-((x-m1+d)**2))/(2*(s**2)))


	return first_peak + second_peak + third_peak


ymeasure = np.array([
-9479552.00000,
-4830927.50000,
-2648416.75000,
-4564425.50000,
-4808560.00000,
-4413367.50000,
-7302069.50000,
-13373112.00000,
-12818494.00000,
-5524100.00000,
 8175881.50000,
  22911592.00000,
   45246636.00000,
    63502692.00000,
     68905768.00000,
      80913288.00000,
       128582080.00000,
        209280080.00000,
	 297325728.00000,
	  341618464.00000,
	   305735712.00000,
	    287061792.00000,
	     409812928.00000,
	      610178432.00000,
	       667685376.00000,
	        506181888.00000,
		 291122144.00000,
		  191029872.00000,
		   202621488.00000,
		    225991680.00000,
		     196307392.00000,
		      127446272.00000,
		       68427760.00000,
		        40777184.00000,
			 31211356.00000,
			  24656236.00000,
			   18197344.00000,
			    14506482.00000,
			     14894635.00000,
			      15040497.00000,
			       10582719.00000,
			        4098529.00000,
				 3147637.00000,
				  3731190.00000,
				   7546011.00000,
				    9563360.00000,
				     6626809.00000
	])



x = np.arange(47.0)
max = ymeasure.max()
params = curve_fit(pyruvate_func, x, ymeasure, p0=([0.5*max, max, 5, 23.5, 10]))

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

ypredict = pyruvate_func(xpredict, p[0], p[1], p[2], p[3], p[4])


plt.plot(x,ymeasure, linewidth=5.0)
plt.plot(xpredict, ypredict, linewidth=5.0)
plt.show()
