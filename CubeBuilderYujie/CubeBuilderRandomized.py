import argparse
import csv
import math
import random
import sys


# finds the distance between GPS points in meters
def GPSDist(lat1, lon1, lat2, lon2):
    earthRadiusM = 6371000
    dLat = (lat2 - lat1) * math.pi / 180;
    dLon = (lon2 - lon1) * math.pi / 180;
    lat1 = lat1 * math.pi / 180;
    lat2 = lat2 * math.pi / 180;

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(
        lat2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    return earthRadiusM * c


def bearing(lat1, lon1, lat2, lon2):

    lat1r = math.radians(lat1)
    lat2r = math.radians(lat2)
    dLon = math.radians(lon2 - lon1)
    y = math.sin(dLon) * math.cos(lat2r)
    x = math.cos(lat1r) * math.sin(lat2r) - math.sin(lat1r) * math.cos(lat2r) * math.cos(dLon)
    brng = math.atan2(y, x);
    brng = brng * 180 / math.pi;
    brng = (brng + 360) % 360
    return brng


def findNSEW(lat1, lon1, dataset):
    points = []
    for data in dataset:
        brng = bearing(lat1, lon1, float(data[2]), float(data[3]))
        dist = GPSDist(lat1, lon1, float(data[2]), float(data[3]))
        points.append([dist, brng, data[0]])

    direction = [[], [], [], [], [], [], [], []]

    # sort by dist low to high
    points.sort(key=lambda x: x[0])
    for point in points[1:]:
        brng = point[1]
        key = point[2]

        # north
        if 345 <= brng or brng < 15:
            if not direction[0]:
                direction[0] = key
        # north east
        elif 15 <= brng < 75:
            if not direction[1]:
                direction[1] = key
        # east
        elif 75 <= brng < 105:
            if not direction[2]:
                direction[2] = key
        # southeast
        elif 105 <= brng < 165:
            if not direction[3]:
                direction[3] = key
        # south
        elif 165 <= brng < 195:
            if not direction[4]:
                direction[4] = key
        # southwest
        elif 195 <= brng < 255:
            if not direction[5]:
                direction[5] = key
        # west
        elif 255 <= brng < 285:
            if not direction[6]:
                direction[6] = key
        # northwest
        elif 285 <= brng < 345:
            if not direction[7]:
                direction[7] = key

    return direction

def randomize(selectedSize,dataset):
    randomNum,randomData = [],[]
    sizeIndex = 0
    while sizeIndex < selectedSize and sizeIndex < len(dataset[0]):
        r = random.randint(0, len(dataset[0]))
        if r not in randomNum:
            sizeIndex += 1
            randomNum.append(r)

    for i in randomNum:
        for data in dataset[0][1:]:
            if data[0] == i:
                randomData.append(data)
    return randomData

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputCSV', type=str, help='Input data file (.csv)')
    parser.add_argument('outputCSV', type=str, help='Output data file (.csv)')
    parser.add_argument('selectedSize', type=int, help='The number of images you want to select (int)')
    args = parser.parse_args()
    print("File", args.inputCSV, "successfully imported")

    dataset = []
    inputfile = sys.argv[1]
    outfile = sys.argv[2]
    selectedSize = int(sys.argv[3])

    with open(inputfile, 'r') as data:
        reader = csv.reader(data)
        dataset.append(list(reader))

    count = 0
    for data in dataset[0][1:]:
        data.insert(0,count)
        count += 1

    randomData = randomize(selectedSize,dataset)

    for data in randomData:
        dirList = findNSEW(float(data[2]), float(data[3]), randomData)
        data.append(dirList)

    with open(outfile, "w") as of:
        wr = csv.writer(of, quoting=csv.QUOTE_MINIMAL)
        for data in randomData:
            wr.writerow(data)


if __name__ == "__main__":
    main()
