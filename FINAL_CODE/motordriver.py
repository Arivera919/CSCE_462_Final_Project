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
        self.currentDir = self.CW

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
        sleep(self.sleepTime)

        if (self.currentDir == self.CW):
            self.steps = self.steps + 1
        elif (self.currentDir == self.CCW):
            self.steps = self.steps - 1

    def change_dir(self, direction=-1, first_hit=False):
        sleep(0.5)

        if (direction == self.CW):
            GPIO.output(self.dir, self.CCW)
            self.currentDir = self.CCW
        elif (direction == self.CCW):
            GPIO.output(self.dir, self.CW)
            self.currentDir = self.CW
        else:
            if (self.currentDir == self.CW):
                GPIO.output(self.dir, self.CCW)
                self.currentDir = self.CCW
            elif (self.currentDir == self.CCW):
                GPIO.output(self.dir, self.CW)
                self.currentDir = self.CW
        
        if first_hit:
            self.sleepTime = self.sleepTime / 2

    def check_win(self):
        return self.steps == self.goal or self.steps == -1 * self.goal

    def reset_motor(self):
        if(self.steps > 0):
            sleep(0.5)
            GPIO.output(self.dir, self.CCW)
            self.currentDir = self.CCW
        elif(self.steps < 0):
            sleep(0.5)
            GPIO.output(self.dir, self.CW)
            self.currentDir = self.CW

        while (self.steps != 0):
            self.motor_step()

        self.sleepTime = 0.005/4
        
        #GPIO.cleanup()

    def normal_start(self):
        for x in range(400):
            self.motor_step()
        
        self.change_dir(self.currentDir, False)

        for x in range(400):
            self.motor_step()


        


