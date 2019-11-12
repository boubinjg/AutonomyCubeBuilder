from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
import argparse
import csv
import os, os.path

import sys

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / float(dms[0][1])
    minutes = dms[1][0] / float(dms[1][1]) / 60.0
    seconds = dms[2][0] / float(dms[2][1]) / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 8)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging


geoTags = {}
index = 0
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='File which has the pics in it.')
args = parser.parse_args

with open('data.csv',mode='w') as data_file:
	fieldnames = ['Number', 'Image', 'Latitude', 'Longitude']
	writer = csv.DictWriter(data_file, fieldnames = fieldnames)
	writer.writeheader()

	fileForPics = args.file
	for fileName in os.listdir(fileForPics):
            coordinates = get_coordinates(get_geotagging(get_exif(fileForPics+fileName)))
            lat, lon = coordinates
            writer.writerow({'Number': index,'Image': fileName, 'Latitude': lat, 'Longitude': lon})	
            index = index + 1
print ("Completed")
