import os, os.path
import shutil
import argparse
import string
import random

"""
	This program will generate random data sets from a given input. BEWARE, it will change the names of the 
	given files to random names, then copy them into a big pool, and then generate datasets out of that big pool.
	
	Inputs: 
	src - Parent Directory with data
	dest - Directory where you want your datasets to be placed
	# Of Datasets - How many datasets you want
	Lenght of Each Data Set - How many pictures should be in each dataset
"""
parser = argparse.ArgumentParser()
parser.add_argument('src', type=str, help='Parent Directory that includes all the Sortes.')
parser.add_argument('dest', type=str, help='Directory where you would like everything to be compiled to.')
parser.add_argument('numOfDatasets', type=int, help='Number of Datasets you would like created.')
parser.add_argument('lenOfDatasets', type=int, help='How much data should the Datasets have?')
args = parser.parse_args()

dest = args.dest
src = args.src
numOfDataSets = args.numOfDatasets
lenOfDataSets = args.lenOfDatasets

oneFileDest = dest+'oneFile/'

if not (os.path.exists(oneFileDest)):
    os.mkdir(oneFileDest)

print("Renaming ...")
for dir_name in os.listdir(src):
	src_files = src + dir_name+"/"
	for file_name in os.listdir(src_files):
		randomString = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
		rnddst = src_files+ randomString + ".jpg"
		rndsrc = src_files + file_name
		os.rename(rndsrc,rnddst)
		
numOfFiles = 0
print("Consolidating ...")
for dir_name in os.listdir(src):
	src_files = src + dir_name+"/"
	for file_name in os.listdir(src_files):
		full_file_name = os.path.join(src_files, file_name)
    		if os.path.isfile(full_file_name):
          		shutil.copy(full_file_name, oneFileDest)
            	numOfFiles = numOfFiles + 1
            

print("Making datasets ...")

numsCalled = []

for xthSet in range(numOfDataSets):
	newDest = dest+'DS'+str(xthSet)
	os.mkdir(newDest)
	listOfRandoms = [0] * lenOfDataSets;
	for x in range(lenOfDataSets):
		number = random.randint(1,numOfFiles)
		while (number in numsCalled):
			number = random.randint(1,numOfFiles)
		numsCalled.append(number)
		listOfRandoms[x] = number
	src_files = os.listdir(oneFileDest)
	relList = [src_files[i-1] for i in listOfRandoms]
	for file_name in relList:
 		full_file_name = os.path.join(oneFileDest, file_name)
		if os.path.isfile(full_file_name):
        		shutil.copy(full_file_name, newDest)
