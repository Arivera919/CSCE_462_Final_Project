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

    def detectHit(self, sel):
        #filter out no signal: 0.0
        v = self.chan0.voltage if sel==0 else self.chan1.voltage
        v2 = self.chan0.voltage if sel==0 else self.chan1.voltage
        hit = v < self.threshold and v != 0.0 and v2 < self.threshold and v2 != 0.0
        

        if hit:
            print(f"Detected hit at channel {sel}. V = {v}V")
            sleep(.1)
        return 


if __name__ == "__main__":
    t = Target(3) 
    time = 0

    while True:
        t.detectHit(0)
        t.detectHit(1)
        sleep(.1)

