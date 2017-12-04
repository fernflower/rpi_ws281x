import time
import types

import neopixel

import extdevinterface
import utils


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


class ForcedStopException(Exception):
    pass


def monitor_forced_stop(f):
    def wrapper(*args, **kwargs):
        strip = args[0]
        if strip._stop_immediately:
            strip._stop_immediately = False
            raise ForcedStopException()
        return f(*args, **kwargs)
    return wrapper


class Ledring(extdevinterface.ExternalDevice):
    config_section = "ledring"
    basic_colors = {"blue": Color(0, 0, 255),
                    "green": Color(0, 255, 0),
                    "red": Color(255, 0, 0),
                    "dim": Color(250, 238, 221),
                    "neutral-red": Color(255, 76, 78),
                    "yellow": Color(250, 156, 78),
                    "off": Color(0, 0, 0)}

    def __init__(self, *args, **kwargs):
        self.curr_mode = None
        self._stop_immediately = False
        super(Ledring, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        # search in basic_colors
        attr_str = attr.replace("_", "-")
        if attr_str in self.basic_colors:
            return self.basic_colors[attr_str]
        return super(Ledring).getattr(attr)

    def stop_immediately(self):
        self._stop_immediately = True
        self.curr_mode = None

    @property
    def modes(self):
        return {"test": self.default_test_cycle,
                "off": lambda : self.apply_color("off")}

    def init(self):
        self.strip = neopixel.Adafruit_NeoPixel(
                int(self.params.leds),
                int(self.params.din),
                int(self.params.freq),
                int(self.params.dma),
                int(self.params.invert),
                int(self.params.brightness))
        self.strip.begin()
        return self.strip

    def run(self, mode):
        if mode == self.curr_mode:
            print("Mode is already %s" % mode)
            # already in this mode, exiting
            return
        if mode in self.modes:
            self.curr_mode = mode
            self.modes[mode]()

    def apply_color(self, color):
        if isinstance(color, str):
            color = self.basic_colors.get(color, "off")
        for i in range(0, self.strip.numPixels()):
            self.strip.setPixelColor(i, color.neo_color)
        self.strip.show()

    def turn_off(self):
        self.apply_color(basic_colors["off"])

    @monitor_forced_stop
    # borrowed from jgarff's library as is, thanks pal!
    def colorWipe(self, color, wait_ms=50):
        color = color.neo_color
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    @monitor_forced_stop
    def gradient(self, color1, color2, wait_ms=100):
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
            self.colorWipe(next_color, wait_ms)
            color_tuple = [(next_color[i] + directions[i]) for i in range(0, 3)]
            if any(x > 255 or x < 0 for x in color_tuple):
                return
            next_color = Color(*color_tuple)

    @monitor_forced_stop
    # borrowed from jgarff's library as is, thanks pal!
    def theaterChase(self, color, wait_ms=50, iterations=10):
        color = color.neo_color
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    @monitor_forced_stop
    # partly borrowed from jgarff's library
    def default_test_cycle(self):
        # Color wipe animations.
        self.colorWipe(Color(255, 0, 0))  # Red wipe
        self.colorWipe(Color(0, 255, 0))  # Blue wipe
        self.colorWipe(Color(0, 0, 255))  # Green wipe
        # Theater chase animations.
        self.theaterChase(Color(127, 127, 127))  # White theater chase
        self.theaterChase(Color(127,   0,   0))  # Red theater chase
        self.theaterChase(Color(0, 0, 127))  # Blue theater chase
        # make sure mode is cleared
        self.curr_mode = None

def main():
    leds = Ledring()
    print('Press Ctrl-C to quit.')
    try:
        # leds.apply_color("neutral-red")
        # leds.apply_color("off")
        color1 = leds.neutral_red
        color2 = leds.dim
        leds.gradient(color1, color2)
        leds.gradient(color2, color1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        leds.apply_color("dim")


if __name__ == "__main__":
    main()
