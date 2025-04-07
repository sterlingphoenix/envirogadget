#!/home/pi/.virtualenvs/pimoroni/bin/python

import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

from bme280 import BME280
import st7735
from subprocess import PIPE, Popen
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
from enviroplus import gas
from enviroplus.noise import Noise


# Temp/humidity sensor
bme280 = BME280()
# Light/proximity sensor
ltr559 = LTR559()
# Noise sensor
noise = Noise()

update_sec=10
sleep_step=0.5
current_sec=0
mode = 1
offset = 10

# LCD screen
display = st7735.ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)

def showtext(m):
	# Text settings.
	font_size = 45
	font = ImageFont.truetype(UserFont, font_size)
	#text_color = (255, 255, 255)
	#back_color = (0, 170, 170)

	#text_color = (0, 50, 50)
	#back_color = (255, 130, 0)

	back_color = (0, 0, 0)
	text_color = (255, 130, 0)

	message = m

	# Calculate text position
	x1, y1, x2, y2 = font.getbbox(message)
	size_x = x2 - x1
	size_y = y2 - y1

	x = (WIDTH - size_x) / 2
	y = (HEIGHT / 2) - (size_y / 2)	- offset

	# Draw background rectangle and write text.
	draw.rectangle((0, 0, 160, 80), back_color)
	draw.text((x, y), message, font=font, fill=text_color)
	display.display(img)

# Initialize display
display.begin()

WIDTH = display.width
HEIGHT = display.height

img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

showtext("INIT")


# Keep running.
try:
	while True:
		#print("   TOCK")
		rawtemp = bme280.get_temperature() - 2
		temp = "{:.1f}".format(rawtemp)
		temp = temp+u'\N{DEGREE SIGN}'+"C"
		rawhumidity = bme280.get_humidity()
		humidity = "{:.1f}".format(rawhumidity)
		humidity = humidity+"%H"
		if mode == 1:
			text = temp
		elif mode == 2:
			text = humidity

		showtext(text)

		while current_sec < update_sec:
			current_sec += sleep_step
			time.sleep(sleep_step)
			proximity = ltr559.get_proximity()
			#print("Tick! Prox: "+str(proximity))
			if proximity > 300:
				#print("Proxxed!")
				current_sec = update_sec
				if mode == 1:
					mode = 2
				elif mode == 2:
					mode = 1

		current_sec = 0

# Turn off backlight on control-c
except KeyboardInterrupt:
    display.set_backlight(0)


