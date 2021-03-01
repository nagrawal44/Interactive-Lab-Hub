import time
from datetime import datetime, timedelta
import subprocess
import digitalio
import board
from time import strftime, sleep
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

clock = datetime.now()
timezone = 0
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    clock = datetime.now() + timedelta(hours=timezone)
    # clock = datetime.datetime.now()
    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py
    y = top
    # clock_str = str(clock)
    draw.text((x,y), format(clock, '%H:%M:%S'), font=font, fill="#FFFFFF")
    y += font.getsize(str(clock))[1]
    draw.text((x,y), "Top adds hour", font=font, fill="#FFFFFF")
    y += font.getsize(str(clock))[1]
    draw.text((x,y), "Bottom subtracts hour", font=font, fill="#FFFFFF")
   # print(strftime("%m/%d/%Y %H:%M:%S"), end="", flush=True)
   # print("\r", end="", flush=True)
    #if buttonA.value and buttonB.value:
     #   backlight.value = False
    #else:
     #   backlight.value = True
    if buttonA.value and not buttonB.value:
       y = top
       draw.rectangle((0, 0, width, height), outline=0, fill=0)
       timezone = timezone - 1
       clock = datetime.now() + timedelta(hours=timezone)
       draw.text((x,y), "Subtracted one hour", font=font, fill="#FFFFFF")
    if buttonB.value and not buttonA.value:
       y = top
       draw.rectangle((0, 0, width, height), outline=0, fill=0)
       timezone = timezone + 1
       clock = datetime.now() + timedelta(hours=timezone)
       draw.text((x,y), "Added one hour", font=font, fill="#FFFFFF")
    if not buttonA.value and not buttonB.value:
       draw.text((x,y), clock, font=font, fill="#FFFFFF")
    # Display image.
    disp.image(image, rotation)
    time.sleep(1)

