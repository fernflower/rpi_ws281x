# Pull base image
FROM resin/rpi-raspbian:wheezy

COPY . /rpi_ws281x

# Install dependencies
RUN apt-get update && apt-get install -y \
        build-essential \
        python \
        python-dev \
        python-pip \
        python-virtualenv \
        scons \
        swig \
        --no-install-recommends && \
        rm -rf /var/lib/apt/lists/* && \
        virtualenv -p /usr/bin/python2.7 /venv && \
        /venv/bin/pip install -r /rpi_ws281x/requirements.txt && \ 
        cd /rpi_ws281x/rpi_ws281x && scons && \
        cd /rpi_ws281x/rpi_ws281x/python && python setup.py build 

# set link in venv to built neopixel lib
RUN /bin/sh -c "echo \"/rpi_ws281x/rpi_ws281x/python/build/lib.linux-armv6l-2.7/\" > /venv/lib/python2.7/site-packages/rpi_ws281x_driver.pth"

# Define working directory
WORKDIR /rpi_ws281x

CMD bash -c "source /venv/bin/activate && python button.py"
