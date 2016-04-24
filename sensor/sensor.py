# Description:
# Signatur: tirgger_reading: -> number
# Purpose: Function triggers a distance-measurement and returns the calculated distance in [cm].
# Author:   Niklas Trzaska,
#           Code for function from 
#           http://www.bytecreation.com/blog/2013/10/13/raspberry-pi-ultrasonic-sensor-hc-sr04
#           and modified according purpose.


import time
import RPi.GPIO as GPIO

def trigger_reading():
    
    # Warnings disabled
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BCM)
    
        
    # Define used GPIOs  
    GPIO.setup(17,GPIO.OUT)
    GPIO.setup(27,GPIO.IN)
    GPIO.output(17, GPIO.LOW)
        
    # Avoid crashs     
    time.sleep(0.5)
    
    # Send signal    
    GPIO.output(17, True)
        
    # Sensor expects a puls-length of 10Us 
    time.sleep(0.00001)
        
    # Stop pulse
    GPIO.output(17, False)
    
    # listen to the input pin.
    # 0:= no input
    # 1:= input measured
    while GPIO.input(27) == 0:
        signaloff = time.time()
  
    while GPIO.input(27) == 1:
        signalon = time.time()
        
    # calculate distance
    timepassed = signalon - signaloff
        
    # convert distance into cm
    distance = timepassed * 17000
        
    return distance

    GPIO.cleanup()



# When the code is executed, __main__ will be compared to the scope from which the call came (__name__).
# The terminal has the scope '__main__', so the measurement will start.
# If the file is imported into another one, the scope changed and the file will not be executed during the import.
if __name__=='__main__':
    print(trigger_reading())
