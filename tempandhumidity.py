import time
from datetime import datetime
import grovepi
import math    
import json

import logging
from logging.handlers import TimedRotatingFileHandler

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logpath = 'logs/tempandhumidity.log'

          # change this depending on your sensor type - see header comment

def main():
    
    
    # logHandler = logging.StreamHandler()
    logHandler = TimedRotatingFileHandler(logpath, when="d", interval=1, backupCount=5)

    formatter = CustomJsonFormatter('(timestamp) (level) (name) (message)')
    # formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    while True:
        checktempandhumidity()
        time.sleep(1)

def checktempandhumidity():
    pin = 7
    dht_sensor_type = 0   

    try:
        [temp,humidity] = grovepi.dht(pin,dht_sensor_type)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity = %.02f%%"%(temp, humidity))
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            fahrenheit = temp * 1.8 + 32

            logger.info({"temperature": fahrenheit, "humidity": humidity})
        

    except IOError:
        print "Error"

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