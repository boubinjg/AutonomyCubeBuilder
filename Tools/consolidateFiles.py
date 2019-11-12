import os
import shutil
import argparse

"""
Script which consolidates all files from a given path into one generic directory.

Example: 
Given a dataset which is broken up into Sortes, will go through each Sorte and copy all the pictures into one single larger directory.
"""

parser = argparse.ArgumentParser()
parser.add_argument('src', type=str, help='Parent Directory that includes all the Sortes.')
parser.add_argument('dest', type=str, help='Directory where you would like everything to be compiled to.')
args = parser.parse_args()

dest = args.dest
src = args.src

for dir_name in os.listdir(src):
	src_files = src + dir_name+"/"
	for file_name in os.listdir(src_files):
		full_file_name = os.path.join(src_files, file_name)
		print(full_file_name)
    		if os.path.isfile(full_file_name):
    	   		shutil.copy(full_file_name, dest)
