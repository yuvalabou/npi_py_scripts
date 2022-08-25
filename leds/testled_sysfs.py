# Import Twisted mainloop
from time import sleep

from pysysfs.boards import NANOPI_NEO_3
from pysysfs.const import OUTPUT

from pysysfs.Controller import Controller
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

controller = Controller()
controller.available_pins = NANOPI_NEO_3

# Allocate a pin as Output signal
led = controller.alloc_pin(79, OUTPUT)


def main():
    """Main."""
    led.high()
    sleep(1)
    led.low()
    sleep(1)


lc = LoopingCall(main)
lc.start(0.1)

reactor.run()
