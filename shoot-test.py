from time import sleep
import sys
import threading
import RPi.GPIO as GPIO
import random

def motor_thread(DIR, STEP, goal, hit_event, win_event):
    CW = 1
    CCW = 0

    steps = 0
    sleepTime = 0.005/8

    hit_event.wait() #target will not move until a hit is detected
    
    currentDir = random.choice([CW, CCW])
    GPIO.output(DIR, currentDir)
    hit_event.clear()

    while not win_event.is_set():

        if (hit_event.is_set() and currentDir == CW):
            sleep(0.5)
            GPIO.output(DIR, CCW)
            currentDir = CCW
            sleepTime = sleepTime / 2
            hit_event.clear()
        elif (hit_event.is_set() and currentDir == CCW):
            sleep(0.5)
            GPIO.output(DIR, CW)
            currentDir = CW
            sleepTime = sleepTime / 2
            hit_event.clear()

        GPIO.output(STEP, GPIO.HIGH)
        sleep(sleepTime) #determine how fast stepper motor will run
        GPIO.output(STEP, GPIO.LOW)
        sleep(sleepTime)
        if (currentDir == CW):
            steps = steps + 1
        elif (currentDir == CCW):
            steps = steps - 1
        #print(steps)
        #print(sleepTime_1)

        if ((steps == goal or steps == goal*-1) and (not win_event.is_set())):
            win_event.set()

    #LEDs on targets will flash with the color of the winner
    #Blue = Player 1
    #Red = Player 2

    #After breaking out of loop, target resets itself back to 0
    if(steps > 0):
        sleep(0.5)
        GPIO.output(DIR, CCW)
        currentDir = CCW
    elif(steps < 0):
        sleep(0.5)
        GPIO.output(DIR, CW)
        currentDir = CW

    while (steps != 0):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.005/16)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.005/16)
        if (currentDir == CW):
            steps = steps + 1
        elif (currentDir == CCW):
            steps = steps - 1
        print(steps)


def sensor_thread(hit_event, win_event):

    while not win_event.is_set():
        changer = input("change direction?")#final program will use target class
        if (not win_event.is_set()):
            hit_event.set()
            while hit_event.is_set():
                sleep(0.1)#waits until motor finishes changing direction before allowing another hit


if __name__ == '__main__':
    #motor 1
    #Direction pin
    DIR_1 = 17
    DIR_2 = 23
    #Step pin
    STEP_1 = 27
    STEP_2 = 24

    goal_1 = 9600 #where target's position at center is 0, goal is number of steps needed to get from center to either goal
    goal_2 = 8000

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(DIR_2, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)
    GPIO.setup(STEP_2, GPIO.OUT)

    win_event = threading.Event()
    hit_event1 = threading.Event() #will need a second hit_event when second motor is introduced
    hit_event2 = threading.Event()

    motor1 = threading.Thread(target=motor_thread, args=(DIR_1, STEP_1, goal_1, hit_event1, win_event))
    motor2 = threading.Thread(target=motor_thread, args=(DIR_2, STEP_2, goal_2, hit_event2, win_event))
    sensor1 = threading.Thread(target=sensor_thread, args=(hit_event1, win_event))
    sensor2 = threading.Thread(target=sensor_thread, args=(hit_event2, win_event))

    motor1.start()
    motor2.start()
    sensor1.start()
    sleep(1)
    sensor2.start()

    #waits for win condition to be met and then waits for threads to finish
    #win_event.wait()
    motor1.join()
    motor2.join()
    sensor1.join()
    sensor2.join()

    GPIO.cleanup()
    #sys.exit(0)
