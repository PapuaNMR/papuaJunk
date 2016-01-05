import matplotlib.pyplot as plt 
import numpy as np
import nmrglue as ng
import matplotlib.cm

fighmqc = plt.figure(figsize=(4,3), dpi=200)
#fignoesyplane = plt.figure()

cmap = matplotlib.cm.Blues_r
contour_start = 3000000000
contour_num = 10
contour_factor = 1.4

cl = contour_start * contour_factor ** np.arange(contour_num)

dic,data = ng.pipe.read("4D_Pipe_Files/test%04d%05d.ft4")


ax = fighmqc.add_subplot(111)

#ax.contour(data.transpose(), cl, cmap=cmap, 
#		extent=(ppm_13c_1, ppm_13c_0, ppm_1h_1, ppm_1h_0))




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
	
	if (newx_min < 0): newx_min = 0
	if (newy_min < 0): newy_min = 0
	if (newx_max > data.shape[1]): newx_max = data.shape[1]		
	if (newy_max > data.shape[0]): newy_max = data.shape[0]	

	ax.set_xlim(ppm_1h_1, ppm_1h_0)
	ax.set_ylim(ppm_13c_1, ppm_13c_0)
	fighmqc.canvas.draw()


fighmqc.canvas.mpl_connect('scroll_event', onscroll)

plt.show()
