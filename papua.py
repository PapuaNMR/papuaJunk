import struct
import numpy as np
import sys 
from scipy.ndimage.filters import maximum_filter

# dictionary of pipe parameters
fdata_dic = {
'FDMAGIC': 0,
'FDFLTFORMAT': 1,
'FDFLTORDER': 2,
'FDSIZE': 99,
'FDREALSIZE': 97,
'FDSPECNUM': 219,
'FDQUADFLAG': 106,
'FD2DPHASE': 256,
'FDTRANSPOSED': 221,
'FDDIMCOUNT': 9,
'FDDIMORDER': 24,
'FDDIMORDER1': 24,
'FDDIMORDER2': 25,
'FDDIMORDER3': 26,
'FDDIMORDER4': 27,
'FDPIPEFLAG': 57,
'FDPIPECOUNT': 75,
'FDSLICECOUNT': 443,
'FDFILECOUNT': 442,
'FDFIRSTPLANE': 77,
'FDLASTPLANE': 78,
'FDPARTITION': 65,
'FDPLANELOC': 14,
'FDMAX': 247,
'FDMIN': 248,
'FDSCALEFLAG': 250,
'FDDISPMAX': 251,
'FDDISPMIN': 252,
'FDUSER1': 70,
'FDUSER2': 71,
'FDUSER3': 72,
'FDUSER4': 73,
'FDUSER5': 74,
'FDLASTBLOCK': 359,
'FDCONTBLOCK': 360,
'FDBASEBLOCK': 361,
'FDPEAKBLOCK': 362,
'FDBMAPBLOCK': 363,
'FDHISTBLOCK': 364,
'FD1DBLOCK': 365,
'FDMONTH': 294,
'FDDAY': 295,
'FDYEAR': 296,
'FDHOURS': 283,
'FDMINS': 284,
'FDSECS': 285,
'FDMCFLAG': 135,
'FDNOISE': 153,
'FDRANK': 180,
'FDTEMPERATURE': 157,
'FD2DVIRGIN': 399,
'FDTAU': 199,
'FDSRCNAME': 286,
'FDUSERNAME': 290,
'FDOPERNAME': 464,
'FDTITLE': 297,
'FDCOMMENT': 312,
'FDF2LABEL': 16,
'FDF2APOD': 95,
'FDF2SW': 100,
'FDF2OBS': 119,
'FDF2ORIG': 101,
'FDF2UNITS': 152,
'FDF2QUADFLAG': 56,
'FDF2FTFLAG': 220,
'FDF2AQSIGN': 64,
'FDF2LB': 111,
'FDF2CAR': 66,
'FDF2CENTER': 79,
'FDF2OFFPPM': 480,
'FDF2P0': 109,
'FDF2P1': 110,
'FDF2APODCODE': 413,
'FDF2APODQ1': 415,
'FDF2APODQ2': 416,
'FDF2APODQ3': 417,
'FDF2C1': 418,
'FDF2ZF': 108,
'FDF2X1': 257,
'FDF2XN': 258,
'FDF2FTSIZE': 96,
'FDF2TDSIZE': 386,
'FDF1LABEL': 18,
'FDF1APOD': 428,
'FDF1SW': 229,
'FDF1OBS': 218,
'FDF1ORIG': 249,
'FDF1UNITS': 234,
'FDF1FTFLAG': 222,
'FDF1AQSIGN': 475,
'FDF1LB': 243,
'FDF1QUADFLAG': 55,
'FDF1CAR': 67,
'FDF1CENTER': 80,
'FDF1OFFPPM': 481,
'FDF1P0': 245,
'FDF1P1': 246,
'FDF1APODCODE': 414,
'FDF1APODQ1': 420,
'FDF1APODQ2': 421,
'FDF1APODQ3': 422,
'FDF1C1': 423,
'FDF1ZF': 437,
'FDF1X1': 259,
'FDF1XN': 260,
'FDF1FTSIZE': 98,
'FDF1TDSIZE': 387,
'FDF3LABEL': 20,
'FDF3APOD': 50,
'FDF3OBS': 10,
'FDF3SW': 11,
'FDF3ORIG': 12,
'FDF3FTFLAG': 13,
'FDF3AQSIGN': 476,
'FDF3SIZE': 15,
'FDF3QUADFLAG': 51,
'FDF3UNITS': 58,
'FDF3P0': 60,
'FDF3P1': 61,
'FDF3CAR': 68,
'FDF3CENTER': 81,
'FDF3OFFPPM': 482,
'FDF3APODCODE': 400,
'FDF3APODQ1': 401,
'FDF3APODQ2': 402,
'FDF3APODQ3': 403,
'FDF3C1': 404,
'FDF3ZF': 438,
'FDF3X1': 261,
'FDF3XN': 262,
'FDF3FTSIZE': 200,
'FDF3TDSIZE': 388,
'FDF4LABEL': 22,
'FDF4APOD': 53,
'FDF4OBS': 28,
'FDF4SW': 29,
'FDF4ORIG': 30,
'FDF4FTFLAG': 31,
'FDF4AQSIGN': 477,
'FDF4SIZE': 32,
'FDF4QUADFLAG': 54,
'FDF4UNITS': 59,
'FDF4P0': 62,
'FDF4P1': 63,
'FDF4CAR': 69,
'FDF4CENTER': 82,
'FDF4OFFPPM': 483,
'FDF4APODCODE': 405,
'FDF4APODQ1': 406,
'FDF4APODQ2': 407,
'FDF4APODQ3': 408,
'FDF4C1': 409,
'FDF4ZF': 439,
'FDF4X1': 263,
'FDF4XN': 264,
'FDF4FTSIZE': 201,
'FDF4TDSIZE': 389,
'FD_SEC': 1,
'FD_HZ': 2,
'FD_PPM': 3,
'FD_PTS': 4,
'FD_MAGNITUDE': 0,
'FD_TPPI': 1,
'FD_STATES': 2,
'FD_IMAGE': 3,
'FD_QUAD': 0,
'FD_COMPLEX': 0,
'FD_SINGLATURE': 1,
'FD_REAL': 1,
'FD_PSEUDOQUAD': 2
}

def fdata2dic(fdata):
    """
    Convert a fdata array to fdata dictionary.

    Converts the raw 512x4-byte NMRPipe header into a python dictionary
    with keys as given in fdatap.h

    """
    dic = dict()

    # Populate the dictionary with FDATA which contains numbers
    for key in fdata_dic.keys():
	dic[key] = float(fdata[int(fdata_dic[key])])
    
    # make the FDDIMORDER
    dic["FDDIMORDER"] = [dic["FDDIMORDER1"], dic["FDDIMORDER2"],
                         dic["FDDIMORDER3"], dic["FDDIMORDER4"]]

    # Populate the dictionary with FDATA which contains strings
    dic["FDF2LABEL"] = struct.unpack('8s', fdata[16:18])[0].rstrip('\x00')
    dic["FDF1LABEL"] = struct.unpack('8s', fdata[18:20])[0].rstrip('\x00')
    dic["FDF3LABEL"] = struct.unpack('8s', fdata[20:22])[0].rstrip('\x00')
    dic["FDF4LABEL"] = struct.unpack('8s', fdata[22:24])[0].rstrip('\x00')
    dic["FDSRCNAME"] = struct.unpack('16s', fdata[286:290])[0].rstrip('\x00')
    dic["FDUSERNAME"] = struct.unpack('16s', fdata[290:294])[0].rstrip('\x00')
    dic["FDTITLE"] = struct.unpack('60s', fdata[297:312])[0].rstrip('\x00')
    dic["FDCOMMENT"] = struct.unpack('160s', fdata[312:352])[0].rstrip('\x00')
    dic["FDOPERNAME"] = struct.unpack('32s', fdata[464:472])[0].rstrip('\x00')
    return dic

def readnmrPipe(infile):
	if infile:
		data = np.fromfile(infile, 'float32')
	else:
		stdin = sys.stdin.read()
		data = np.frombuffer(stdin, dtype=np.float32)
	if data[2] - 2.345 > 1e-6:  # check for byteswap
		data = data.byteswap()

	#header = data[:512]
	#data =  data[512:]

	return data[:512], data[512:]

def findPeaks(data, threshold, size=3, mode='wrap'):
	peaks = []
	if (data.size == 0) or (data.max() < threshold):
		return peaks

	boolsVal = data > threshold

	maxFilter = maximum_filter(data, size=size, mode=mode)
	boolsMax = data == maxFilter

	boolsPeak = boolsVal & boolsMax

	indices = np.argwhere(boolsPeak)

	for position in indices:
		position = tuple(position)
		height = data[position]
		peak = Peak(position, data, height)
		peaks.append(peak)

	return peaks


class Peak:
	def __init__(self, position, data, dataHeight=None, linewidth=None):
		self.position = tuple(position)
		self.data = data
		self.point = tuple([int (round(x)) for x in position])

		if dataHeight is None:
			dataHeight = data[self.point]
		self.dataHeight = dataHeight

		if linewidth is None:
			linewidth = self._calcHalfHeightWidth()
		self.linewidth = linewidth

		self.fitAmplitude = None
		self.fitPosition = None
		self.fitLineWidth = None

	def _calcHalfHeightWidth(self):

		dimWidths = []

		for dim in range(self.data.ndim):
			posA, posB = self._findHalfPoints(dim)
			width = posB-posA
			dimWidths.append(width)

		return dimWidths

	def _findHalfPoints(self, dim):

		height = abs(self.dataHeight)
		halfHt = 0.5 * height
		data = self.data
		point = self.point

		testPoint = list(point)
		posA = posB = point[dim]

		prevValue = height
		while posA > 0:
			posA -= 1
			testPoint[dim] = posA
			value = abs(data[tuple(testPoint)])

			if value <= halfHt:
				posA += (halfHt-value)/(prevValue-value)
				break

			prevValue = value

		lastPoint = data.shape[dim] - 1
		
		prevValue = height
		while posB < lastPoint-1:
			posB +=1
			testPoint[dim] = posB
			value = abs(data[tuple(testPoint)])

			if value <= halfHt:
				posB -+ (halfHt-value)/(prevValue-value)
				break
			
			prevValue = value

		return posA, posB
