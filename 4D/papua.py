import matplotlib.pyplot as plt 
import numpy as np
import nmrglue as ng
import matplotlib.cm

fighmqc = plt.figure(figsize=(4,3), dpi=200)
#fignoesyplane = plt.figure()

cmap = matplotlib.cm.Blues_r
contour_start = 200000
contour_num = 20
contour_factor = 1.2

cl = contour_start * contour_factor ** np.arange(contour_num)

dic,data = ng.pipe.read("13C.1H.sum.dat")

dimensions = [4, 1]

#print "LABEL", dic["FDF1LABEL"], dic["FDF2LABEL"], dic["FDF3LABEL"], dic["FDF4LABEL"]
#print "OBS", dic["FDF1OBS"], dic["FDF2OBS"], dic["FDF3OBS"], dic["FDF4OBS"]
#print "SW", dic["FDF1SW"], dic["FDF2SW"], dic["FDF3SW"], dic["FDF4SW"]
#print "ORIG", dic["FDF1ORIG"], dic["FDF2ORIG"], dic["FDF3ORIG"], dic["FDF4ORIG"]
#print "CAR", dic["FDF1CAR"], dic["FDF2CAR"], dic["FDF3CAR"], dic["FDF4CAR"]
#print "CENTER", dic["FDF1CENTER"], dic["FDF2CENTER"], dic["FDF3CENTER"], dic["FDF4CENTER"]
#print "FTSIZE", dic["FDF1FTSIZE"], dic["FDF2FTSIZE"], dic["FDF3FTSIZE"], dic["FDF4FTSIZE"]
#print "TDSIZE", dic["FDF1TDSIZE"], dic["FDF2TDSIZE"], dic["FDF3TDSIZE"], dic["FDF4TDSIZE"]
#print "OFFPPM", dic["FDF1OFFPPM"], dic["FDF2OFFPPM"], dic["FDF3OFFPPM"], dic["FDF4OFFPPM"]
#print "UNITS", dic["FDF1UNITS"], dic["FDF2UNITS"], dic["FDF3UNITS"], dic["FDF4UNITS"]

#print "FDDIMCOUNT", dic["FDDIMCOUNT"]
print "FDDIMORDER", dic["FDDIMORDER"]
#print "FDDIMORDERN", dic["FDDIMORDER1"], dic["FDDIMORDER2"], dic["FDDIMORDER3"], dic["FDDIMORDER4"]

ppm_1h_1 = dic["FDF" + str(dimensions[0]) + "ORIG"] / dic["FDF" + str(dimensions[0]) + "OBS"]
ppm_1h_0 = ppm_1h_1 + dic["FDF" + str(dimensions[0]) + "SW"] / dic["FDF" + str(dimensions[0]) + "OBS"]
print ppm_1h_0, ppm_1h_1

ppm_13c_1 = dic["FDF" + str(dimensions[1]) + "ORIG"] / dic["FDF" + str(dimensions[1]) + "OBS"]
ppm_13c_0 = ppm_13c_1 + dic["FDF" + str(dimensions[1]) + "SW"] / dic["FDF" + str(dimensions[1]) + "OBS"]
print ppm_13c_0, ppm_13c_1

#uc_dim0 = ng.pipe.make_uc(dic,data,dim=1)
#dim0_0, dim0_1 = uc_dim0.ppm_limits()
#print "Dim 0 limits", dim0_0, dim0_1



ax = fighmqc.add_subplot(111)

ax.contour(data.transpose(), cl, cmap=cmap, 
		extent=(ppm_1h_0, ppm_1h_1, ppm_13c_0, ppm_13c_1))

ax.set_xlim(ppm_1h_0, ppm_1h_1)
ax.set_ylim(ppm_13c_0, ppm_13c_1)

matplotlib.rcParams.update({'font.size': 8})

def onscroll(event):
	x, y, step = event.xdata, event.ydata, event.step
	ymin, ymax = ax.get_ylim()
	xmin, xmax = ax.get_xlim()
	xsize = xmax - xmin
	ysize = ymax - ymin
	xcenter = (xmax+xmin)/2
	ycenter = (ymax+ymin)/2
	xsize = xsize * (0.8**step)
	ysize = ysize * (0.8**step)
	x_new_center = xcenter + (x-xcenter)*0.2*step
	y_new_center = ycenter + (y-ycenter)*0.2*step
	newx_min = x_new_center-(xsize/2); newx_max = x_new_center+(xsize/2)
	newy_min = y_new_center-(ysize/2); newy_max = y_new_center+(ysize/2) 
	
	if (newx_min > ppm_1h_0): newx_min = ppm_1h_0
	if (newy_min > ppm_13c_0): newy_min = ppm_13c_0
	if (newx_max < ppm_1h_1): newx_max = ppm_1h_1		
	if (newy_max < ppm_13c_1): newy_max = 	ppm_13c_1

	ax.set_xlim(newx_min, newx_max)
	ax.set_ylim(newy_min, newy_max)

	fighmqc.canvas.draw()
	fighmqc.tight_layout()

fighmqc.canvas.mpl_connect('scroll_event', onscroll)

plt.show()
