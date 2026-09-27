# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This demo will fill the screen with white, draw a black box on top
and then print Hello World! in the center of the display

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
"""

import board # pyright: ignore[reportMissingImports]
import busio # pyright: ignore[reportMissingImports]
import digitalio # pyright: ignore[reportMissingImports]
import time 
import ntplib # pyright: ignore[reportMissingImports]
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone
import zoneinfo

import adafruit_sharpmemorydisplay # pyright: ignore[reportMissingImports]

def utc_epoch():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3)
        real_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
        return real_time
    except Exception as e:
        print(f"couldn't get time: {e}")
        return None

BLACK = 0
WHITE = 255

BORDER = 5
FONTSIZE = 10

spi = busio.SPI(board.SCK, MOSI=board.MOSI)
scs = digitalio.DigitalInOut(board.D6)  # inverted chip select

display = adafruit_sharpmemorydisplay.SharpMemoryDisplay(spi, scs, 400, 240)

display.fill(1)
display.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (display.width, display.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

draw.rectangle((0, 0, display.width, display.height), fill=WHITE)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

init_wall = datetime.now()
real_time = utc_epoch()

while True:
    
    wall = datetime.now()
    deltawall = wall - init_wall
    
    t = real_time + deltawall
    print(t)

    bbox = font.getbbox(t)
    font_width = bbox[2] - bbox[0]
    font_height = bbox[3] - bbox[1]
    
    x = (display.width // 2) - (font_width // 2)
    y = (display.height // 2) - (font_height // 2)
    
    draw.rectangle((0, 0, display.width, display.height), fill=WHITE)
    draw.text((x, y), text, font=font, fill=BLACK)
    
    display.image(image)
    display.show()
    time.sleep(0.5)

