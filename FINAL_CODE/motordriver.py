import RPi.GPIO as GPIO
from time import sleep

class Motor:

    CW = 1
    CCW = 0

    def __init__(self, DIR, STEP, goal):
        #setup GPIO pins for motor
        self.dir = DIR
        self.step = STEP
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

        #current direction of motor 1(CW) by default
        self.currentDir = CW

        #number of steps the motor has taken
        self.steps = 0

        #determines frequency of step signal
        self.sleepTime = 0.005/4

        #the distance the target needs to travel to win
        self.goal = goal

    def motor_step(self):
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.sleepTime)
        GPIO.output(self.step, GPIO.LOW)

        if (self.currentDir == CW):
            self.steps = self.steps + 1
        elif (self.currentDir == CCW):
            self.steps = self.steps - 1

    def change_dir(self, direction=-1, first_hit=false):
        sleep(0.5)

        if (direction == CW):
            GPIO.output(self.dir, CCW)
            self.currentDir = CCW
        elif (direction == CCW):
            GPIO.output(self.dir, CW)
            self.currentDir = CW
        else:
            if (self.currentDir == CW):
                GPIO.output(self.dir, CCW)
                self.currentDir = CCW
            elif (self.currentDir == CCW):
                GPIO.output(self.dir, CW)
                self.currentDir = CW
        
        if not first_hit:
            self.sleepTime = self.sleepTime / 2

    def check_win(self):
        return self.steps == self.goal or self.steps == -1 * self.goal

    def reset_motor(self):
        if(self.steps > 0):
            sleep(0.5)
            GPIO.output(self.dir, CCW)
            self.currentDir = CCW
        elif(self.steps < 0):
            sleep(0.5)
            GPIO.output(self.dir, CW)
            self.currentDir = CW

        while (self.step != 0):
            self.motor_step()
        
        #GPIO.cleanup()

    def normal_start(self):
        for x in range(400):
            self.motor_step()
        
        self.change_dir(self.currentDir, False)

        for x in range(400):
            self.motor_step()


        


