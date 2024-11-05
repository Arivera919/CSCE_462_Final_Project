#class abstracting away SPI and hit detection logic

from time import sleep 
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class Target:

    #threshold: value, in volts, of a detected hit
    def __init__(self, threshold)
        # create the spi bus
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        self.cs = digitalio.DigitalInOut(board.D22)

        # create the mcp object
        self.mcp = MCP.MCP3008(spi, cs)

        # create analog input channels
        self.chan0 = AnalogIn(mcp, MCP.P0)
        self.chan1 = AnalogIn(mcp, MCP.P1)

        self.threshold = threshold

    def detectHit():
        hit0 = self.chan0.voltage < self.threshold
        hit1 = self.chan1.voltage < self.threshold
        return(hit0, hit1)


if __name__ == "__main__":
    while True:
        hits = detectHit()
        if hits[0]:
            print("Target 0 hit!")
        if hits[1]:
            print("Target 1 hit")
        

