from time import sleep
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
        print(steps)
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
        elif (currentDire == CCW):
            steps = steps - 1
        print(steps)


def sensor_thread(hit_event, win_event):

    while not win_event.is_set():
        changer = input("change direction? (y/n):")#final program will use target class
            if (changer == "y" and (not win_event.is_set())):
                hit_event.set()
                while hit_event.is_set():
                    sleep(0.1)#waits until motor finishes changing direction before allowing another hit


if __name__ == '__main__':
    #motor 1
    #Direction pin
    DIR_1 = 17
    #Step pin
    STEP_1 = 27

    goal = 19200 #where target's position at center is 0, goal is number of steps needed to get from center to either goal

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(DIR_1, GPIO.OUT)
    GPIO.setup(STEP_1, GPIO.OUT)

    win_event = threading.Event()
    hit_event = threading.Event() #will need a second hit_event when second motor is introduced

    motor1 = threading.Thread(target=motor_thread, args=(DIR_1, STEP_1, goal, hit_event, win_event))
    sensor1 = threading.Thread(target=sensor_thread, args=(hit_event, win_event))

    motor1.start()
    sensor1.start()

    #waits for win condition to be met and then waits for threads to finish
    win_event.wait()
    motor1.join()
    sensor1.join()

    GPIO.cleanup()