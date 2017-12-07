import os
import subprocess
import time

import button
import ledring
import servo


def main():
    a_button = button.Button()
    a_servo = servo.Servo()
    a_ledring = ledring.Ledring()
    pressed = True
    is_on = False
    while True:
        time.sleep(0.1)
        while a_button.is_pressed():
            print("button pressed")
            pressed = True
        if pressed:
            is_on = not is_on
            print("Button is now %s" % ("on" if is_on else "off"))
            if is_on:
                a_ledring.apply_color("neutral-red")
                if a_servo._started:
                    a_servo.stop()
            else:
                a_ledring.apply_color("yellow")
                a_servo.start()
            pressed = False


if __name__ == "__main__":
    main()

