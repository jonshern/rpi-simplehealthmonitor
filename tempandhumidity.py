import time
from datetime import datetime
import grovepi
import math    
import json
import csv
import os.path

import logging
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logpath = '/home/pi/logs/tempandhumidity.log'
csvfilepath = '/home/pi/logs/tempandhumidity.csv'
location = 'Office'

          # change this depending on your sensor type - see header comment

def main():
    
    
    # logHandler = logging.StreamHandler()
    logHandler = TimedRotatingFileHandler(logpath, when="d", interval=1, backupCount=5)


    # formatter = logging.Formatter('%(asctime)s,  %(name)s ,  %(levelname)s ,  %(message)s')

    # quicksight wants a csv
    formatter = CustomJsonFormatter('(timestamp) (level) (name) (message)')
    # formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    checktempandhumidity()

def checktempandhumidity():
    pin = 7
    dht_sensor_type = 0   

    try:
        [temp,humidity] = grovepi.dht(pin,dht_sensor_type)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity = %.02f%%"%(temp, humidity))
            now = datetime.now().strftime('%Y-%m-%d %H:%M')

            fahrenheit = temp * 1.8 + 32

            # logger.info(str(fahrenheit) + "," + str(humidity))
            logger.info({"temperature": fahrenheit, "humidity": humidity})
            writetocsv(csvfilepath, now, location, fahrenheit, humidity)

    except IOError:
        print "Error"


def writetocsv(filename, timestamp, location, temperature, humidity):
    fieldnames = ['timestamp', 'location', 'temperature', 'humidity']

    if not os.path.isfile(filename):
        with open(filename, 'a') as csvfile:           
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'timestamp': timestamp, 'location': location, 'temperature': temperature, 'humidity': humidity})


    # if the file name does not exist create it



class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
            log_record['location'] = "Office"
            
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


if __name__ == '__main__':
    main()