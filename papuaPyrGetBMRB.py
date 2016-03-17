#!/usr/bin/env python
import papua
import urllib2
import numpy as np
import matplotlib.pyplot as plt

response = urllib2.urlopen('http://www.bmrb.wisc.edu/ftp/pub/bmrb/statistics/chem_shifts/selected/aasel/ALA_CA_link.txt')

html = response.read().splitlines()

shifts = []

for line in html:
	fields =  line.split()
	shifts.append(float(fields[0]))

npshifts = np.array(shifts)


print papua.aa_dic['A'][0]

