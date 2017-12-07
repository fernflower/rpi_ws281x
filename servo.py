from RPIO import PWM

import extdevinterface
import utils


class MyPWMServo(PWM.Servo):
    # NOTE(ivasilevskaya) ledring driven by neopixels library
    # was conflicting with servo unless a non-pwd delay_hw is set.
    # So subclassing PWM.Servo class for the only purpose of
    # overriding default DELAY_VIA_PWM flag in PWM.setup()
    def __init__(self, dma_channel=0, subcycle_time_us=20000,
                 pulse_incr_us=10, delay_type=PWM.DELAY_VIA_PCM):
        """
        Makes sure PWM is setup with the correct increment granularity and
        subcycle time.
        """
        self._dma_channel = dma_channel
        self._subcycle_time_us = subcycle_time_us
        if PWM.is_setup():
            _pw_inc = PWM.get_pulse_incr_us()
            if not pulse_incr_us == _pw_inc:
                raise AttributeError(("Error: PWM is already setup with pulse-"
                        "width increment granularity of %sus instead of %sus")\
                         % (_pw_inc, self.pulse_incr_us))
        else:
            PWM.setup(pulse_incr_us=pulse_incr_us, delay_hw=delay_type)


class Servo(extdevinterface.ExternalDevice):
    config_section = "servo"

    def init(self):
        self.pin = int(self.params.pin)
        self.servo = MyPWMServo(int(self.params.dma))
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
