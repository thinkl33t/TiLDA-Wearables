import database
import pyb

class Colour(object):
	def __init__(self, r=0, g=0, b=0):
		if type(r) is 'str':
			self.set_hex(r)
		else:
			self._colour = [r,g,b]

	def set_hex(self, colourstring):
		colourstring = colourstring.strip()
		if colourstring[0] == '#': colourstring = colourstring[1:]
		r, g, b = colourstring[:2], colourstring[2:4], colourstring[4:]
		r, g, b = [int(n, 16) for n in (r, g, b)]
		self._colour = [r, g, b]

	def get_tuple(self):
		return self._colour

	def get_hex(self):
		return "#%02X%02X%02X" % tuple(self._colour)

	def get_neo(self):
		return int("%02X%02X%02X" % tuple(self._colour), 16)

	def set_r(self, value):
		self._colour[0] = value

	def set_g(self, value):
		self._colour[1] = value

	def set_b(self, value):
		self._colour[2] = value

	def __str__(self):
		return self.get_hex()

def Wheel(pos):
	position = 255 - pos

	if (position < 85):
		return Colour(255 - position * 3, 0, position * 3)

	if (position < 170):
		position = position - 85
		return Colour(0, position * 3, 255 - position * 3)

	position = position - 170
	return Colour(position * 3, 255 - position * 3, 0)

def tick():
	global wheelColour, ledcount, sequence, ledpin

	pin = pyb.Pin(ledpin)
	neo = pyb.Neopix(pin)

	leds = [0x000000] * ledcount

	if (sequence == "rainbow"):
		wheelColour = (wheelColour + 8) & 255
		for ledNumber in range(0, ledcount):
			pos = ((ledNumber*8)+wheelColour)
			pos = pos & 255
			leds[ledNumber] = Wheel(pos).get_neo()
	elif (sequence == "matrix"):
		for ledNumber in range(0, ledcount):
			led_green = (pyb.rng() & 255)
			led_colour = Colour(0, led_green, 0)
			if led_green < 230:
				led_colour.set_g(int(led_green / 8))
			if led_green > 253:
				led_colour.set_hex('#ffffff')
			leds[ledNumber] = led_colour.get_neo()
	elif (sequence == "colour"):
		colour = database.database_get("led-colour", "#ffffff")
		tmp_colour = Colour()
		tmp_colour.set_hex(colour)
		leds = [tmp_colour.get_neo()] * ledcount
	neo.display(leds)

# 67 LEDs because thats how many i have on my lanyard
ledcount = database.database_get("led-count", 67)
# show the rainbow sequence by default
sequence = database.database_get("led-seq-name", "rainbow")
# default to pb13, which is the onboard neopixel
ledpin = database.database_get("led-port", "PB13")

wheelColour = 0
period = database.database_get("led-period", 50)
