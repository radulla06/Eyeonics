import os
import base64
import requests
import time
import sys


count = 0

while (True):
    stream1 = os.popen('fswebcam /home/pi/Eyeonics/Images/image' + str(count) + '.jpg')
    output1 = stream1.read()
    my_string1 = ""
            
    with open('/home/pi/Eyeonics/Images/image' + str(count) + '.jpg',"rb") as img_file1:
        my_string1 = base64.b64encode(img_file1.read())
    
    count+=1
    time.sleep(3)
