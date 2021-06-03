# Import Twisted mainloop
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

# Import this package objects
from pysysfs.Controller import Controller
from pysysfs.const import OUTPUT
from pysysfs.boards import NANOPI_NEO_3
from time import sleep


controller = Controller()
controller.available_pins = NANOPI_NEO_3

# Allocate a pin as Output signal
led = controller.alloc_pin(79, OUTPUT)


def main():
    led.high()
    sleep(1)
    led.low()
    sleep(1)

lc = LoopingCall(main)
lc.start(0.1)

reactor.run()
