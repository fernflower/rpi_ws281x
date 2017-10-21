import time
import utils

import neopixel

PARAMS = utils.read_config("ledring")

class Color(object):
    def __init__(self, r, g, b, w=0):
        # XXX FIXME why is color order (rgb) wrong?!
        # a quick workaround, but what the hell?
        self.neo_color = neopixel.Color(g, r, b, w)
        self.r = r
        self.g = g
        self.b = b
        self.w = w

    def to_tuple(self):
        return (self.r, self.g, self.b, self.w)

    def __getitem__(self, i):
        t = self.to_tuple()
        return t[i]

    def __eq__(self, other):
        return self.to_tuple() == other.to_tuple() 

    def __hash__(self):
        return hash(self.to_tuple())

    def __str__(self):
        return "%s" % str(self.to_tuple())

    def __repr__(self):
        return self.__str__()


BASIC_COLORS = {"blue": Color(0, 0, 255), 
                "green": Color(0, 255, 0),
                "red": Color(255, 0, 0),
                "dim": Color(250, 238, 221),
                "off": Color(0, 0, 0)}


def init():
    # returns object representing the ring
    # Create NeoPixel object with appropriate configuration.
    strip = neopixel.Adafruit_NeoPixel(
            int(PARAMS.leds), int(PARAMS.din), int(PARAMS.freq),
            int(PARAMS.dma),
            int(PARAMS.invert), int(PARAMS.brightness))
    # Intialize the library (must be called once before other functions).
    strip.begin()
    return strip


def _apply_color(strip, color):
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color.neo_color)
    strip.show()


def turn_off(strip):
    _apply_color(strip, BASIC_COLORS["off"])


def make_dim(strip):
    _apply_color(strip, BASIC_COLORS["dim"])


# borrowed from jgarff's library as is, thanks pal!
def colorWipe(strip, color, wait_ms=50):
    color = color.neo_color
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)


def gradient(strip, color1, color2, wait_ms=100):
    delta = 30
    directions = []
    for i in range(3):
        if color1[i] == color2[i]:
            d = 0
        else:
            d = -1 * delta if color1[i] > color2[i] else delta
        directions.append(d)
    next_color = color1
    while next_color != color2:
        colorWipe(strip, next_color, wait_ms)
        color_tuple = [(next_color[i] + directions[i]) for i in range(0, 3)]
        if any(x > 255 or x < 0 for x in color_tuple):
            return
        next_color = Color(*color_tuple)

# borrowed from jgarff's library as is, thanks pal!
def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

# borrowed from jgarff's library as is, thanks pal!
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


# borrowed from jgarff's library as is, thanks pal!
def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


# borrowed from jgarff's library as is, thanks pal!
def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)


# borrowed from jgarff's library as is, thanks pal!
def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def test_cycle(strip):
    # Color wipe animations.
    colorWipe(strip, Color(255, 0, 0))  # Red wipe
    colorWipe(strip, Color(0, 255, 0))  # Blue wipe
    colorWipe(strip, Color(0, 0, 255))  # Green wipe
    # Theater chase animations.
    theaterChase(strip, Color(127, 127, 127))  # White theater chase
    theaterChase(strip, Color(127,   0,   0))  # Red theater chase
    theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
    # Rainbow animations.
    rainbow(strip)
    rainbowCycle(strip)
    theaterChaseRainbow(strip)


def main():
    strip = init()
    print('Press Ctrl-C to quit.')
    color1 = BASIC_COLORS["green"]
    color2 = BASIC_COLORS["blue"]
    try:
        while True:
            gradient(strip, color1, color2)
            gradient(strip, color2, color1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        make_dim(strip)


if __name__ == "__main__":
    main()
