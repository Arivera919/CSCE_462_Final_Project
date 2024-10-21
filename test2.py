import RPi.GPIO as GPIO
from time import sleep
import os

#other motor:
#A+ = Black
#A- = Green
#B+ = Red
#B- = Blue
#1.50 Amps
#1600 pulse/rev

#motor 2
#Direction pin
DIR_2 = 17
#Step pin
STEP_2 = 27

#clockwise vs counterclockwise
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR_2, GPIO.OUT)
GPIO.setup(STEP_2, GPIO.OUT)

#how to set direction
GPIO.output(DIR_2, CCW)

sleepTime_2 = 0.005
steps_2 = 0
changeDir_2 = false
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
        steps_2 = steps_2 + 1
        print(steps_2)
        print(sleepTime_2)

        #needs time to change direction
        if (steps_2 == 3200):
            sleep(0.5)
            changeDir_2 = True
            steps_2 = 0

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
