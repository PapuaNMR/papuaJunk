import matplotlib.pyplot as plt 
import numpy as np
import nmrglue as ng
import matplotlib.cm

fighmqc = plt.figure(figsize=(4,3), dpi=200)
#fignoesyplane = plt.figure()

cmap = matplotlib.cm.Blues_r
contour_start = 500000
contour_num = 20
contour_factor = 1.4

cl = contour_start * contour_factor ** np.arange(contour_num)

dic,data = ng.pipe.read("/Users/scott/Dropbox/GB1_DCN/2/test.ft2")




ax = fighmqc.add_subplot(111)
#print ("x ", data.shape[1], "y ", data.shape[0])

ax.contour(data, cl, cmap=cmap, 
		extent=(0, data.shape[1] - 1, 0, data.shape[0] - 1))

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

	ax.set_xlim(newx_min, newx_max)
	ax.set_ylim(newy_min, newy_max)
	fighmqc.canvas.draw()


fighmqc.canvas.mpl_connect('scroll_event', onscroll)

plt.show()
