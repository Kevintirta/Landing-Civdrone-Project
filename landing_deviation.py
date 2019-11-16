import json
import sys
import os
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from math import sin, cos, sqrt, atan2, radians

# hide tkinter box
top = Tk()
top.withdraw()

# user changable parameters
DIAMETER_OF_EARTH = 637.1 * pow(10,6)
target_coordinates = (-35.3632296, 149.1652651) # (lat, long)

def dist(data, target_lat, target_lon):
    """
    dist returns distance between input data & longtitude, latitude of target location

    :param
        data: dictionary contains latitude and longitude for each different time
        target_lat: latitude of target location
        target_lon: longitude of target location

    :return
        distance in centimeters
    """
    lat = radians(data['lat']/pow(10,7))
    lon = radians(data['lon']/pow(10,7))
    dev_lat = target_lat - lat
    dev_lon = target_lon - lon

    # a is the square of half the chord length between two points while c is the angular distance in radians
    a = sin(dev_lat / 2)**2 + cos(target_lat) * cos(lat) * sin(dev_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = DIAMETER_OF_EARTH * c

    return(distance)

def getJSON(filepath):
        with open(filepath,'r') as fp:
            return json.load(fp)

if os.path.isfile('landingData.JSON'):
    file = getJSON('landingData.JSON')
else:
    messagebox.showwarning("Alert", "Input 'landingData.JSON' file does not exist. \n\nPlease make sure the input file in the same directory.")
    sys.exit()

target_lat = radians(target_coordinates[0])
target_lon = radians(target_coordinates[1])

list_dist = []
list_time = []

for data in file:
    distance = dist(data,target_lat, target_lon)
    list_dist.append(distance)
    list_time.append(data['deltaTime'])

plt.plot(list_time,list_dist,label='deviation')
plt.title('Time vs Deviation Plot')
plt.xlabel('time (second)')
plt.ylabel('deviation (cm)')
plt.grid(color='black', linestyle='-', linewidth=0.1)
plt.axhline(y=0,color='r',alpha=0.4,label='target')
plt.legend(loc='upper right')
plt.show()
