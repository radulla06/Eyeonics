import os
import base64
import requests
import time
import sys
import RPi.GPIO as GPIO

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

count = 1

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    distance = round(distance/2.54)
 
    return distance

while (True):
    stream1 = os.popen('fswebcam /home/pi/Eyeonics/Images/image' + str(count) + '.jpg')
    output1 = stream1.read()
    my_string1 = ""
            
    with open('/home/pi/Eyeonics/Images/image' + str(count) + '.jpg',"rb") as img_file1:
        my_string1 = base64.b64encode(img_file1.read())
        
    dist = distance()
    print ("Measured Distance = %.1f in" % dist)
    
    text = "There is an object " + str(dist) + " inches away from you."
    os.system('espeak -s 150 "' + text + '"')
    
    count+=1
    time.sleep(4)
