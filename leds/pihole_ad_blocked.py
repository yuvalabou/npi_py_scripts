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


def check_log_tail_result() -> None:
    """Tails PiHole log file."""
    if p.poll(1):
        line = f.stdout.readline().decode("utf-8")
        if GRAVITY in line and FALSE_POS not in line:
            blocked(line)
        if FORWARDED in line and FALSE_POS not in line:
            forwarded(line)
        if CACHED in line and FALSE_POS not in line:
            cached(line)


def forwarded(log_line, blink_time=0.2) -> None:
    """Blink on forwarded quary."""
    print("Forwarded  ==>  " + log_line)
    yellow.high()
    sleep(blink_time)
    yellow.low()


def cached(log_line, blink_time=0.2) -> None:
    """Blink on cached quary."""
    print("Cached  ==>  " + log_line)
    green.high()
    sleep(blink_time)
    green.low()


def blocked(log_line, blink_time=0.2) -> None:
    """Blink on blocked quary."""
    print("Ad Blocked!  ==>  " + log_line)
    red.high()
    sleep(blink_time)
    red.low()


# Main loop
lc = LoopingCall(check_log_tail_result)
lc.start(0.1)

reactor.run()
