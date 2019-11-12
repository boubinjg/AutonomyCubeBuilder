import sys
import csv
import math

#finds the distance between GPS points in meters
def GPSDist(lat1, lon1, lat2, lon2):
    earthRadiusM = 6371000
    dLat = (lat2-lat1) * math.pi/180;
    dLon = (lon2-lon1) * math.pi/180;
    lat1 = lat1 * math.pi/180;
    lat2 = lat2 * math.pi/180;

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2);
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a));
    return earthRadiusM * c

def bearing(lat1, lon1, lat2, lon2):
    dLon = (lon2-lon1)
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) *math.cos(lat2) * math.cos(dLon)
    brng = math.atan2(y, x);

    brng = brng * 180/math.pi;
    brng = (brng + 360)%360

    return brng

def findNSEW(lat1, lon1, dataset):
    points = []
    for data in dataset[0][1:]:
        brng = bearing(lat1, lon1, float(data[2]), float(data[3]))
        dist = GPSDist(lat1, lon1, float(data[2]), float(data[3]))
        #print([dist,brng])
        #print(data)
        points.append([dist,brng, data[0]])

    NSEW = [[],[],[],[]]

    #sort by dist low to high
    points.sort(key=lambda x: x[0])

    for point in points[1:]:
        dist = point[0]
        brng = point[1]
        key = point[2]

        #east
        if(345 <= brng or brng < 15):
            if NSEW[2] == []:
                NSEW[2] = key
                #print([brng, dist])

        elif(75 <= brng < 105):
            if NSEW[0] == []:
                NSEW[0] = key
                #print([brng, dist])

        elif(165 <= brng < 195):
            if NSEW[3] == []:
                NSEW[3] = key
                #print([brng, dist])

        elif(255 <= brng < 285):
            if NSEW[1] == []:
                NSEW[1] = key
                #print([brng, dist])

    return NSEW


dataset = []
f = sys.argv[1]
with open(f, 'r') as data:
    reader = csv.reader(data)
    dataset.append(list(reader))

count = 0
geo = []
for data in dataset[0][1:]:
    data.append(count)
    count+=1

for data in dataset[0][1:]:
    dirList = findNSEW(float(data[2]),float(data[3]), dataset)
    data.append(dirList)
    print(dirList)

outfile = sys.argv[2]
with open(outfile, "w") as of:
    wr = csv.writer(of, quoting=csv.QUOTE_MINIMAL)
    for data in dataset[0][1:]:
        wr.writerow(data)
