#simple test program for adc

from time import sleep 
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D21)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create analog input channels
chan0 = AnalogIn(mcp, MCP.P0)

while True:
    print(chan0.voltage)
    sleep(0.1)
