from RPIO import PWM

import extdevinterface
import utils


class Servo(extdevinterface.ExternalDevice):
    config_section = "servo"

    def init(self):
        self.pin = int(self.params.pin)
        self.servo = PWM.Servo(int(self.params.dma))
        self._started = False
        return self.servo

    def start(self):
        self.servo.set_servo(self.pin, 1800)
        self._started = True

    def stop(self):
        self.servo.stop_servo(self.pin)
        self._started = False


def main():
    try:
        servo = Servo()
        servo.start()
        while True:
            print("La-la-la")
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        servo.stop()


if __name__ == "__main__":
    main()
