# rpi_ws281x

Dockerized 12-led ring + button python app. Uses gpio library for managing rpi pins.
Tested with RGB LED ring WS2812 5050 ordered on Aliexpress and RPi model B+.

## Configuration

(presume you have done with soldering and connecting ledring and button to breadboard and Pi)

Correct button's DIO pin number in [config](config.sample) and you are good to go.

Ledring's gpio pin is currently hardcoded as in original library in [main.c](https://github.com/fernflower/rpi_ws281x/blob/master/rpi_ws281x/main.c#L60) and defaults to rpi's BCM 18 (PWM0).

## Docker part

Build a container with 

``` docker build . -t ws281x ```

Run a container (--privileged is necessary for gpio to access rpi's pins)

``` docker run --privileged --name ws281x -d ws281x ```


