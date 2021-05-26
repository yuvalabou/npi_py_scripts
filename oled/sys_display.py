"""Display basic system information."""

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
import psutil
from PIL import ImageFont
import socket
import subprocess


FONT = ImageFont.truetype("./fonts/DejaVuSansMono.ttf", 18)
# ICON_FONT = ImageFont.truetype("./fonts/fontawesome-webfont.ttf", 10)
IFACE = "eth0"
CMD = "/proc/device-tree/model"

serial = i2c(port=0, address=0x3C)
device = ssd1306(serial)
THERMAL = None

def check_board() -> str:
    with subprocess.Popen(['cat', CMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as line:
        board = line.stdout.readline().decode("utf-8")
        if board == "FriendlyElec NanoPi NEO3":
            THERMAL = "soc_thermal"
        elif board == "FriendlyARM NanoPi NEO 2":
            THERMAL = "cpu_thermal"


def get_bytes(t, iface=IFACE) -> int:
    """Get raw network speed."""
    with open("/sys/class/net/" + iface + "/statistics/" + t + "_bytes", "r") as f:
        data = f.read()
        return int(data)


def net_speed() -> str:
    """Calculate live network speed and provide readable value."""
    tx1 = get_bytes("tx")
    rx1 = get_bytes("rx")
    time.sleep(1)
    tx2 = get_bytes("tx")
    rx2 = get_bytes("rx")
    tx_speed = (tx2 - tx1) / 1000000.0
    rx_speed = (rx2 - rx1) / 1000000.0
    return f"TX:{tx_speed:.2f}\nRX:{rx_speed:.2f}"


def system_stats(device):
    timeout = time.time() + 20
    while True:
        test = 0
        if test == 5 or time.time() > timeout:
            break
        test = test - 1
        with canvas(device) as draw:
            h = 17
            top = (32 - h) / 2

            cpu_usage = psutil.cpu_percent(interval=None)
            draw.text((0, top), "CPU", font=FONT, fill=255)
            draw.rectangle((33, top + 4, 126, top + 16), outline=255, fill=0)
            draw.rectangle((33, top + 4, 33 + cpu_usage, top + 16), outline=255, fill=255)

            top = (((32 - h) + (h * 2)) / 2) + 1
            cpu_temp = psutil.sensors_temperatures()[THERMAL][0].current
            draw.text((0, top), "TMP", font=FONT, fill=255)
            draw.rectangle((33, top + 4, 126, top + 16), outline=255, fill=0)
            draw.rectangle((33, top + 4, 33 + cpu_temp, top + 16), outline=255, fill=255)

            top = (((32 - h) + (h * 3)) / 2) + 10
            mem = psutil.virtual_memory().percent
            draw.text((0, top), "RAM", font=FONT, fill=255)
            draw.rectangle((33, top + 4, 126, top + 16), outline=255, fill=0)
            draw.rectangle((33, top + 4, 33 + mem, top + 16), outline=255, fill=255)

            time.sleep(1)


def net_stats(device):
    timeout = time.time() + 20
    while True:
        test = 0
        if test == 5 or time.time() > timeout:
            break
        test = test - 1
        with canvas(device) as draw:
            w, h = draw.textsize(text=net_speed(), font=FONT)
            left = (128 - w) / 2
            top = (32 - h) / 4
            draw.text((left, top), net_speed(), font=FONT, fill=255)

            time.sleep(1)


if __name__ == "__main__":
    try:
        while True:
            system_stats(device)
            net_stats(device)
    except KeyboardInterrupt:
        pass
