import time
import grovepi
import math    
          # change this depending on your sensor type - see header comment

def main():
    checktempandhumidity()

def checktempandhumidity():
    pin = 7
    dht_sensor_type = 0   

    try:
        [temp,humidity] = grovepi.dht(pin,dht_sensor_type)
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temp = %.02f C humidity = %.02f%%"%(temp, humidity))

    except IOError:
        print "Error"

if __name__ == '__main__':
    main()