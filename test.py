import RPi.GPIO as GPIO
from time import sleep
import os

#motor with wires:
#A+ = Black
#A- = Green
#B+ = Red
#B- = Blue
#2 Amps
# 800 pulse/rev

#other motor:
#A+ = Black
#B+ = Green
#A- = Blue
#B- = Red
#1.50 Amps

#motor 1
#Direction pin
DIR_1 = 17
#Step pin
STEP_1 = 27

#motor 2
#DIR_2 =
#STEP_2 =

#clockwise vs counterclockwise
CW = 1
CCW = 0

GPIO.setmode(GPIO.BCM)

GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(STEP_1, GPIO.OUT)
#GPIO.setup(DIR_2, GPIO.OUT)
#GPIO.setup(STEP_2, GPIO.OUT)

#how to set direction
GPIO.output(DIR_1, CW)
#GPIO.output(DIR_2, CCW)

sleepTime_1 = 0.005
steps_1 = 0
changeDir_1 = False
currentDir_1 = CW

#sleepTime_2 = 0.005
#steps_2 = 0
#changeDir_2 = false
#currentDir_2 = CCW

try:
    while True:
        #sleep(1)
        #GPIO.output(DIR_1, CW)
        
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
        #elif (changeDir_2 and currentDir_2 == CW):
        #    GPIO.output(DIR_2, CCW)
        #    currentDir_2 = CCW
        #    changeDir_2 = false
        #    sleepTime_2 = sleepTime_2 / 2
        #elif (changeDir_2 and currentDir_2 == CCW):
        #    GPIO.output(DIR_2, CW)
        #    currentDir_2 = CW
        #    changeDir_2 = false
        #    sleepTime_2 = sleepTime_2 / 2

        GPIO.output(STEP_1, GPIO.HIGH)
        sleep(sleepTime_1) #determine how fast stepper motor will run
        GPIO.output(STEP_1, GPIO.LOW)
        sleep(sleepTime_1)
        steps_1 = steps_1 + 1
        print(steps_1)
        print(sleepTime_1)

        #needs time to change direction
        if (steps_1 == 1600):
            sleep(0.5)
            changeDir_1 = True
            steps_1 = 0

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()
