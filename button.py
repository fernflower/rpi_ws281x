import os
import signal
import subprocess
import time

import RPi.GPIO as IO

import extdevinterface


class Button(extdevinterface.ExternalDevice):
    config_section = "button"

    def init(self):
        self._dio = int(self.params.dio)
        IO.setmode(IO.BCM)
        IO.setup(self._dio, IO.IN, pull_up_down=IO.PUD_DOWN)

    def is_pressed(self):
        # as pull down resistor in initial scheme is used,
        # 1 means button is pressed
        state = IO.input(self._dio)
        return state


def main():
    button = Button()
    pressed = True
    is_on = False
    child = None
    while True:
        time.sleep(0.1)
        while button.is_pressed():
            print("button pressed")
            pressed = True
        if pressed:
            is_on = not is_on
            print("Button is now %s" % ("on" if is_on else "off"))
            if is_on and not child:
                cmd = ["python", "ledring.py"]
                child = subprocess.Popen(cmd)
            elif not is_on:
                if child:
                    os.kill(child.pid, signal.SIGINT)
                    child = None
            pressed = False


if __name__ == "__main__":
    main()
