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
        parser.add_argument('-data', '--data_file', help='Input Data File')
	parser.add_argument('-shifts', '--shifts_file', help='Input shifts file (csv file)')
<<<<<<< Updated upstream
	parser.add_argument('-seq', '--sequence_file', help='Sequence file (one letter, new line)')
	args = vars(parser.parse_args())
=======
	parser.add_argument('-seq', '--sequence_file', help='Input Sequence File')
        args = vars(parser.parse_args())
>>>>>>> Stashed changes

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
		if Data[0] and  Data[1] and Data[3] and Data[4] and Data[0][0] != '#':
			shifts_ppm.append([Data[0], Data[1], Data[4], Data[3]]) # H C N order


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


#print xsw_ppm, xcar_ppm, ysw_ppm, ycar_ppm, zsw_ppm, zcar_ppm

#x_shift_ppm = 8.328
#y_shift_ppm = 57.536
#z_shift_ppm = 121.634
line_num = 0
while line_num < len(shifts_ppm):

	x_shift_ppm, y_shift_ppm, z_shift_ppm = float(shifts_ppm[line_num][1]), float(shifts_ppm[line_num][2]), float(shifts_ppm[line_num][3])

	x_right_ppm = xcar_ppm + 0.5*xsw_ppm

	x_point = round((1.0-((x_shift_ppm - xcar_ppm)/(x_right_ppm - xcar_ppm)))*(0.5*dic['FDF2FTSIZE']) - dic['FDF2X1'] + 0.0)

	y_point = round(dic['FDF3FTSIZE']/2.0 + ((ycar_ppm - y_shift_ppm)/ysw_ppm)*dic['FDF3FTSIZE'] - 1.0)

	z_point = round(dic['FDF1FTSIZE']/2.0 + ((zcar_ppm - z_shift_ppm)/zsw_ppm)*dic['FDF1FTSIZE'] - 1.0)

	#print x_point, y_point, z_point


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



	bestCoord = [z_point, x_point]

	maxCa = 0

	for i in [x_point-2, x_point-1, x_point, x_point+1, x_point+2]:
		for j in [z_point-2, z_point-1, z_point, z_point+1, z_point+2]:
			Ca = data3D[j,(y_point-15):(y_point+16),i]
			if Ca.max() > maxCa:
				maxCa = Ca.max()
				bestCoord = [j, i]
	#			print Ca.max(), j, i
	#			else:
	#			print Ca.max(), j, i

	z_point, x_point = bestCoord

	#print z_point, x_point
	
	Ca = data3D[z_point,(y_point-16):(y_point+17),x_point]



	def pyruvate_func(x, k13, k2, s13, s2, m1, d):
		
		first_peak = (k13)*np.exp((-((x-m1-d)**2))/(2*(s13**2)))
		second_peak = (k2)*np.exp((-((x-m1)**2))/(2*(s2**2)))
		third_peak = (k13)*np.exp((-((x-m1+d)**2))/(2*(s13**2)))

		return first_peak + second_peak + third_peak




	#ymeasure = Ca[(890-13):(890+14)]

	x = np.arange(33.0)
	max = Ca.max()


	if max > 20000000:

		try:	
			params = curve_fit(pyruvate_func, x, Ca, 
					p0=([0.35*max, max, 1.5, 1.5, 16.5, 4.3]),
			
				#	sigma=1.0/np.log(Ca),
				#	absolute_sigma=False,
			
					bounds=([0.000*max, 0.5*max, 1.0, 1.0, 14, 3.0],[0.6*max, 1.22*max, 3.0, 3.0, 17, 5.8]),
					method='dogbox',
					max_nfev=10000
					)

			p = params[0]
			SDerr = np.sqrt(np.diag(params[1]))
			print 'Line number', line_num, 'Amino acid', shifts_ppm[line_num][0], p
	
			fit_font = {'fontname':'monospace', 'size':'9'}


               		xpredict = np.arange(0, 31.0, 0.01)
                	ypredict = pyruvate_func(xpredict, p[0], p[1], p[2], p[3], p[4], p[5])


			if SDerr[0]/p[0] <= 0.5 and SDerr[1]/p[1] <= 0.5:

	     	           	plt.plot(x,Ca, linewidth=5.0)
        	        	plt.plot(xpredict, ypredict, linewidth=5.0)

				plt.figtext(.15,.85,'k13='+'%.3E' % p[0]+' +/- '+'%.3E' % SDerr[0], **fit_font)
				plt.figtext(.15,.80,'k2 ='+'%.3E' % p[1]+' +/- '+'%.3E' % SDerr[1], **fit_font)
				plt.figtext(.15,.75,'s13='+'%.3E' % p[2]+' +/- '+'%.3E' % SDerr[2], **fit_font)
				plt.figtext(.15,.70,'s2 ='+'%.3E' % p[3]+' +/- '+'%.3E' % SDerr[3], **fit_font)
				plt.figtext(.15,.65,'cen='+'%.3E' % p[4]+' +/- '+'%.3E' % SDerr[4], **fit_font)
				plt.figtext(.15,.60,'dis='+'%.3E' % p[5]+' +/- '+'%.3E' % SDerr[5], **fit_font)
				plt.figtext(.15,.87,sequence[int(shifts_ppm[line_num][0])-1]+str(int(shifts_ppm[line_num][0])), **fit_font)

				aa = sequence[int(shifts_ppm[line_num][0])-1]
				num = shifts_ppm[line_num][0]

				plt.savefig('fittings/'+aa+num+'.pdf')
				plt.close()
		
				res = sequence[int(shifts_ppm[line_num][0])-1]
				spectra_amino_dic[res].append(p[0]/p[1]*100)

		except RuntimeError:
			print("Error - curve_fit failed", 'Amino acid', shifts_ppm[line_num][0])
	
			p = params[0]

			#xpredict = np.arange(0, 31.0, 0.01)
			#ypredict = pyruvate_func(xpredict, p[0], p[1], p[2], p[3], p[4], p[5])

			plt.plot(x,Ca, linewidth=5.0)
			#plt.plot(xpredict, ypredict, linewidth=5.0)

		#	plt.plot(Ca)

			plt.show()

	line_num += 1

for key in spectra_amino_dic:
	if len(spectra_amino_dic[key]) != 0:
		print key, np.mean(spectra_amino_dic[key]), np.std(spectra_amino_dic[key]), len(spectra_amino_dic[key])
		x = np.linspace(np.mean(spectra_amino_dic[key])-4*np.std(spectra_amino_dic[key]), np.mean(spectra_amino_dic[key])+4*np.std(spectra_amino_dic[key]), 100)
		y = mlab.normpdf(x,np.mean(spectra_amino_dic[key]), np.std(spectra_amino_dic[key]))
		#y = y/y.max()
		plt.fill_between(x,y, 0, alpha=0.25)
plt.savefig('fittings/distros.pdf')
plt.show()


#### Now lets gather the BMRB chemical shift into for CAs


aa_space = np.zeros((100, 549))


for aa in spectra_amino_dic:


	three_aa = papua.aa_dic[aa][0]

	response = urllib2.urlopen('http://www.bmrb.wisc.edu/ftp/pub/bmrb/statistics/chem_shifts/selected/aasel/'+three_aa+'_CA_link.txt')

	html = response.read().splitlines()

	shifts = []

	for line in html:
        	fields =  line.split()
		shifts.append(float(fields[0]))

	npshifts = np.array(shifts)

	#spaces = np.arange(npshifts.min(), npshifts.max(), 0.1)
	spaces = np.arange(20, 75, 0.1)
	n, bins, patches = plt.hist(npshifts, spaces)
	plt.close()
#A = np.array([0, 0, 1, 2, 1, 0, 0])
#B = np.array([0, 1, 2, 1, 0, 0, 0])

#print np.outer(A, B)a


	x = np.linspace(0, 100, 100)
	y = mlab.normpdf(x,np.mean(spectra_amino_dic[aa]), np.std(spectra_amino_dic[aa]))
	plt.imshow(np.outer(y,n), cmap='Greys', aspect='auto')
	plt.figtext(.15,.85,'Amino Acid: '+three_aa, **fit_font)
	plt.savefig('fittings/Space_For_'+three_aa+'.pdf')
	plt.close()
	aa_space = aa_space + np.outer(y,n)
	#aa_space = aa_space/aa_space.max()
#print y, n 
	#plt.imshow(aa_space, cmap='Greys')

plt.imshow(aa_space, cmap='Greys', aspect='auto')
plt.show()


