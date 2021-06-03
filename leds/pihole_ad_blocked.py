"""App to blink an LED each time a quary has been blocked."""
import subprocess
from select import poll
from time import sleep

from pysysfs.boards import NANOPI_NEO_2
from pysysfs.const import OUTPUT
from pysysfs.Controller import Controller
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

LOG_FILE = "/home/stack/pihole/log/pihole.log"
GRAVITY = "gravity"
FORWARDED = "forwarded"
CACHED = "cached"
FALSE_POS = "read /etc/pihole/gravity.list"
DISABLE_FILE = "/etc/pihole/gravity.list.bck"

controller = Controller()
controller.available_pins = NANOPI_NEO_2

red = controller.alloc_pin(203, OUTPUT)
yellow = controller.alloc_pin(200, OUTPUT)
green = controller.alloc_pin(198, OUTPUT)

f = subprocess.Popen(
    ["tail", "-F", LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
p = poll()
p.register(f.stdout)


def checkLogTailResult() -> None:
    """Tails PiHole log file."""
    if p.poll(1):
        line = f.stdout.readline().encode("utf-8")
        if GRAVITY in line and FALSE_POS not in line:
            blocked(line)
        if FORWARDED in line and FALSE_POS not in line:
            forwarded(line)
        if CACHED in line and FALSE_POS not in line:
            cached(line)


def forwarded(logLine, blinkTime=0.2) -> None:
    """Blink on forwarded quary."""
    print("Forwarded  ==>  " + logLine)
    yellow.high()
    sleep(blinkTime)
    yellow.low()


def cached(logLine, blinkTime=0.2) -> None:
    """Blink on cached quary."""
    print("Cached  ==>  " + logLine)
    green.high()
    sleep(blinkTime)
    green.low()


def blocked(logLine, blinkTime=0.2) -> None:
    """Blink on blocked quary."""
    print("Ad Blocked!  ==>  " + logLine)
    red.high()
    sleep(blinkTime)
    red.low()


# Main loop
lc = LoopingCall(checkLogTailResult)
lc.start(0.1)

reactor.run()
