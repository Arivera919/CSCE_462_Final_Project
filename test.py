import RPi.GPIO as GPIO
from time import sleep
import os

#motor with wires:
#A+ = Black
#A- = Green
#B+ = Red
#B- = Blue
#2 Amps
#1600 pulse/rev

#motor 1
#Direction pin
DIR_1 = 17
#Step pin
STEP_1 = 27

#clockwise vs counterclockwise
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)

#how to set direction
GPIO.output(DIR_1, CW)


sleepTime_1 = 0.005
steps_1 = 0
changeDir_1 = False
currentDir_1 = CW

try:
    while True:
        
        if (changeDir_1 and currentDir_1 == CW):
            sleep(0.5)
            GPIO.output(DIR_1, CCW)
            currentDir_1 = CCW
            changeDir_1 = False
            sleepTime_1 = sleepTime_1 / 2
        elif (changeDir_1 and currentDir_1 == CCW):
            sleep(0.5)
            GPIO.output(DIR_1, CW)
            currentDir_1 = CW
            changeDir_1 = False
            sleepTime_1 = sleepTime_1 / 2

        GPIO.output(STEP_1, GPIO.HIGH)
        sleep(sleepTime_1) #determine how fast stepper motor will run
        GPIO.output(STEP_1, GPIO.LOW)
        sleep(sleepTime_1)
        steps_1 = steps_1 + 1
        print(steps_1)
        print(sleepTime_1)

        #needs time to change direction
        if (steps_1 == 3200):
            sleep(0.5)
            changeDir_1 = True
            steps_1 = 0

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
