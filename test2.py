import RPi.GPIO as GPIO
from time import sleep
import os

#other motor:
#A+ = Black
#A- = Blue
#B+ = Green
#B- = Red
#1.50 Amps
#800 pulse/rev

#motor 2
#Direction pin
DIR_2 = 23
#Step pin
STEP_2 = 24

#clockwise vs counterclockwise
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)

#how to set direction
GPIO.output(DIR_2, CCW)

sleepTime_2 = 0.005/8
steps_2 = 0
changeDir_2 = False
currentDir_2 = CCW

try:
    while True:
        
        if (changeDir_2 and currentDir_2 == CW):
            sleep(0.5)
            GPIO.output(DIR_2, CCW)
            currentDir_2 = CCW
            changeDir_2 = False
            sleepTime_2 = sleepTime_2 / 2
        elif (changeDir_2 and currentDir_2 == CCW):
            sleep(0.5)
            GPIO.output(DIR_2, CW)
            currentDir_2 = CW
            changeDir_2 = False
            sleepTime_2 = sleepTime_2 / 2

        GPIO.output(STEP_2, GPIO.HIGH)
        sleep(sleepTime_2) #determine how fast stepper motor will run
        GPIO.output(STEP_2, GPIO.LOW)
        sleep(sleepTime_2)
        if (currentDir_2 == CW):
            steps_2 = steps_2 + 1
        elif (currentDir_2 == CCW):
            steps_2 = steps_2 - 1
        print(steps_2)
        #print(sleepTime_2)

        #needs time to change direction
        if (steps_2 == 8000 or steps_2 == -8000):
            sleep(0.5)
            changeDir_2 = True
            #steps_2 = 0

except KeyboardInterrupt:
    print("cleanup")
    if(steps_2 > 0):
        sleep(0.5)
        GPIO.output(DIR_2, CCW)
        currentDir_2 = CCW
    elif(steps_2 < 0):
        sleep(0.5)
        GPIO.output(DIR_2, CW)
        currentDir_2 = CW

    while (steps_2 != 0):
        GPIO.output(STEP_2, GPIO.HIGH)
        sleep(0.005/16)
        GPIO.output(STEP_2, GPIO.LOW)
        sleep(0.005/16)
        if (currentDir_2 == CW):
            steps_2 = steps_2 + 1
        elif (currentDire_2 == CCW):
            steps_2 = steps_2 - 1
        print(steps_2)

    GPIO.cleanup()
