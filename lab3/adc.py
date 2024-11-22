#Heavily inspired by https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script

def fuzzycompare(a, b, tolerance):
    return a + tolerance > b and a - tolerance < b 

import numpy as np
import os
from time import sleep 
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 1
chan1 = AnalogIn(mcp, MCP.P1)

wave = "" #tri, sin, square
prelimWave = "" #require a wave to be detected twice before being outputted - stops weirdness when the input changes
tolerance = .1 #tolerance for comparisons in volts
freq = 0


while True:
    #take some samples
    vals = []
    nozeroes = []
    t = 0
    #chan0.value chan0.voltage
    while t < 2000:
        val = chan1.voltage
        vals.append(val)
        if val != 0: #fixes hardware issue where a bunch of "0.0" floats would get sent every now and then
            nozeroes.append(val)
        t += 1
        sleep(.0001)


    #categorize wave
    newWave = ""
    #check for no signal
    if fuzzycompare(0, np.mean(vals), .1):
        newWave = "No signal"

    dydx = np.gradient(nozeroes)

    #check for square - many of dydx values are zero
    dydx_zeroes = np.mean([fuzzycompare(np.abs(dydx[i]),0, .003) for i in range(len(dydx)) ]) 
    if(dydx_zeroes > .1) and newWave == "":
        newWave = "Square"


    dydx_var = np.var(np.abs(dydx))
    #check for tri - lets say at least 75% of derivative values are the same. this method was too vulnerable to noise
    #dydx_same = np.mean([fuzzycompare(np.abs(dydx[i]), dydx[i+1], .004) for i in range(len(dydx) - 1) ])
    #if(dydx_same > 0.75) and newWave == "":
    var_threshold = .000006025 * freq**2 / 2 #constant is gotten from a quadratic regression of measured variance for sin waves. the /2 adds some wiggle room
    if(dydx_var < var_threshold) and newWave == "":
        newWave = "Triangle"
    #getting a signal but it's squiggly - call it a sin
    if newWave == "":
        newWave = "Sin"


    #this stops the wave reading from bouncing around when the waves change
    if wave != newWave:
        if(newWave != prelimWave):
            prelimWave = newWave
        else:
            wave = newWave

    #detect frequency
    distances = []
    if(wave == newWave and wave != "No signal"): #if we're confident about what the wave is 
        #find peaks
        peaks = [fuzzycompare(np.max(vals), vals[i], .5) for i in range(len(vals))]
        #find distance between peaks
        peak_indices = []
        for i in range(1, len(vals)-1):
            if( not peaks[i-1] and peaks[i]):
                peak_indices.append(i)

        for i in range(1, len(peak_indices)):
            distances.append(peak_indices[i] - peak_indices[i-1])

        #find frequency
        freq = 1425 / np.mean(distances) #manally calibrated constant
    else:
        freq = 0
        
    os.system('clear')
    print("Variance:", dydx_var)
    print("Threshold:", var_threshold)
    #print(dydx_same)
    #print("zeroes", dydx_zeroes)
    #print(vals)
    print(wave)
    print(freq)
   # print(distances)

#print(np.gradient(vals))



    
