import csv
import argparse
import gmplot

parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help="File to read from")
args = parser.parse_args()

picId = []
lat = []
lon = []

with open(args.file, "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for lines in csv_reader:
            picId.append(int(lines[0]))
            lat.append(float(lines[2]))
            lon.append(float(lines[3]))
            
gmap5 = gmplot.GoogleMapPlotter(lat[0], 
                                lon[0], 13) 

for i in picId:
    gmap5.marker(lat[i],lon[i],title=i)

gmap5.draw("output.html")

            
