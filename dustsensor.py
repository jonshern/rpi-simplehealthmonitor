# USAGE
#
# Connect the dust sensor to Port D2 on the GrovePi. The dust sensor only works on that port
# The dust sensor takes 30 seconds to update the new values
#
# the fist byte is 1 for a new value and 0 for old values
# second byte is the concentration in pcs/0.01cf

import time
import grovepi
import atexit
import csv
import os.path
from datetime import datetime 


atexit.register(grovepi.dust_sensor_dis)

csvfilepath = '/home/pi/logs/dustlog.csv'
location = 'Office'


def main():
    print("Reading from the dust sensor")
    grovepi.dust_sensor_en()
    while True:
        try:
            [new_val,lowpulseoccupancy] = grovepi.dustSensorRead()
            if new_val:
                print(lowpulseoccupancy)
                now = datetime.now().strftime('%Y-%m-%d %H:%M')
                writetocsv(csvfilepath, now, location, lowpulseoccupancy)
            time.sleep(10) 

        except IOError:
            print ("Error")




def writetocsv(filename, timestamp, location, dustvalue):
    fieldnames = ['timestamp', 'location', 'dustvalue']

    if not os.path.isfile(filename):
        with open(filename, 'a') as csvfile:           
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'timestamp': timestamp, 'location': location, 'dustvalue': dustvalue})




if __name__ == '__main__':
    main()