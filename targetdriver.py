#class abstracting away SPI and hit detection logic

from time import sleep 
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class Target:

    #threshold: value, in volts, of a detected hit
    def __init__(self, threshold):
        # create the spi bus
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(board.D22)

        # create the mcp object
        self.mcp = MCP.MCP3008(self.spi, self.cs)

        # create analog input channels
        self.chan0 = AnalogIn(self.mcp, MCP.P0)
        self.chan1 = AnalogIn(self.mcp, MCP.P1)

        self.threshold = threshold

    def detectHit(self):
        #filter out no signal: 0.0
        v0 = self.chan0.voltage
        v1 = self.chan1.voltage

        hit0 = v0 < self.threshold and v0 != 0.0
        hit1 = v1 < self.threshold and v1 != 0.0
        return(hit0, hit1)


if __name__ == "__main__":
    t = Target(2.95) 
    time = 0

    while True:
        hits = t.detectHit()
        if hits[0]:
            print(f"Target 0 hit at t = {time}0ms")
            sleep(.5)
        sleep(.01)
        time += 1
        #if hits[1]:
            #print("Target 1 hit")
        

