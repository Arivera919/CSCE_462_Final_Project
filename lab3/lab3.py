import board
import busio
import adafruit_mpu6050
import numpy as np
from os import system

from time import sleep, perf_counter

i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)
steps = 0
stepUp = False

while True:
    #print("Acceleration X: %.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    #print("%.2f" % (np.abs(mpu.acceleration[0])+np.abs(mpu.acceleration[1])+np.abs(mpu.acceleration[2])))
    #print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    try:
        z_a = mpu.acceleration[2]
    except:
        sleep(.5)
        i2c = busio.I2C(board.SCL, board.SDA)
        mpu = adafruit_mpu6050.MPU6050(i2c)

    if(z_a < 7.9 and stepUp):
        stepUp = False
        steps += 1
        sleep(.3)

    if(z_a > 9.7):
        stepUp = True

    print(z_a)
    print(steps)

    sleep(0.01)

    system("clear")
