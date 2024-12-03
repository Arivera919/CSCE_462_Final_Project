from time import sleep
from targetdriver import Target
from motordriver import Motor
import sys
import threading
import RPi.GPIO as GPIO
import random

def motor_thread(motor, hit_event, win_event, error_event):
    
    #the game started normally
    motor.change_dir()
    motor.normal_start()

    while not hit_event.is_set() and not win_event.is_set(): 
        #target will not move until a hit is detected
    
    print("hit!")


    currentDir = random.choice([1, 0])
    motor.change_dir(currentDir, True)
    hit_event.clear()

    while not win_event.is_set() and not error_event.is_set():

        if (hit_event.is_set()):
            motor.change_dir()
            hit_event.clear()
        

        motor.motor_step()

        if (motor.check_win() and (not win_event.is_set())):
            win_event.set()

    #LEDs on targets will flash with the color of the winner
    #Blue = Player 1
    #Red = Player 2

    #After breaking out of loop, target resets itself back to 0
    motor.reset_motor()

    if error_event.is_set():
        motor.normal_start()

    return


def sensor_thread(hit_event1, hit_event2,  win_event, error_event, sensor):

    try:
        
        while not win_event.is_set():
            
            if sensor.detectHit(0) and not hit_event1.is_set():
                hit_event1.set()


            if sensor.detectHit(1) and not win_event.is_set():
                hit_event2.set()

    except:

        error_event.set()
 
    return


if __name__ == '__main__':
    #motor 1 & 2
    #Direction pin
    DIR_1 = 17
    DIR_2 = 23
    #Step pin
    STEP_1 = 27
    STEP_2 = 24

    #where target's position at center is 0, goal is number of steps needed to get from center to either goal
    goal_1 = 9600 
    goal_2 = 8000
    threshold = 2.8 

    motor_1 = Motor(DIR_1, STEP_1, goal_1)
    motor_2 = Motor(DIR_2, STEP_2, goal_2)
    
    targets = Target(threshold)

    win_event = threading.Event()
    hit_event1 = threading.Event()
    hit_event2 = threading.Event()
    error_event = threading.Event()

    while True:
        motor1 = threading.Thread(target=motor_thread, args=(motor_1, hit_event1, win_event, error_event))
        motor2 = threading.Thread(target=motor_thread, args=(motor_2, hit_event2, win_event, error_event))
        sensor = threading.Thread(target=sensor_thread, args=(hit_event1, hit_event2,  win_event, error_event, targets))

        motor1.start()
        motor2.start()
        sensor.start()

        #waits for win condition to be met and then waits for threads to finish
        win_event.wait()
        motor1.join()
        motor2.join()
        sensor.join()

        #reset events
        win_event.clear()
        hit_event1.clear()
        hit_event2.clear()


    print("GAME OVER")
    GPIO.cleanup()
