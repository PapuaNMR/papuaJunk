import numpy as np
import os, sys, argparse

# get the commandline options/flags

def getArgs():

	parser = argparse.ArgumentParser(description='Edits down a Bruker ser file to the FIDs listed after -fid option')
	parser.add_argument('-fs', '--fid_size', help='Size of the FID in total points (R+I)', required=True)
	parser.add_argument('-fl', '--fid_list', nargs='+', help='The FIDs to be included in editted ser file', required=True)
	parser.add_argument('-fn', '--fid_name', nargs=1, help='The name of the Bruker Serial File', required=False, default='ser')
	args = vars(parser.parse_args())

	# Size of direct dimension - probably 2048
	fid_size = args['fid_size']

	# Figure out which FIDs we want to keep
	fid_list = args['fid_list']

	# Get the serial file name, default is 'ser' so if not specified it is 'ser'
	fid_name = args['fid_name']

	return fid_size, fid_list, fid_name


def getSerialFile(file):

	ser = open('ser', 'rb')
	ser_data = ser.read()
	
	return ser_data

def reduceSerialData(fid_size, fid_list, ser_data):

	reduced_data = ""
	for fid in fid_list:
		fid0 = int(fid) - 1
		reduced_data += ser_data[fid0*int(fid_size)*4*4:int(fid)*int(fid_size)*4*4]

	return reduced_data


def writeTruncData(reduced_data, fid_name):
	tr = open('ser'+'.reduced', 'wb')
	tr.write(reduced_data)


def main():

	fid_size, fid_list, fid_name = getArgs()
	ser_data = getSerialFile(fid_name)
	reduced_data = reduceSerialData(fid_size, fid_list, ser_data)
	writeTruncData(reduced_data, fid_name)

main()
