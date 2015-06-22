"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
from RPi import GPIO as gpio
import time
import datetime
from lib.albatross import log
from lib.watcher import Watcher

_log = log.get_logger(__name__)


class PirWatcher(Watcher):
    """Passive Infrared Watcher.

    Watcher that uses an HC-SR501 (or equivalent) passive infrared (PIR) sensor
    to detect motion.

    NOTE: Applications using this watcher must be run as root because gpio
    accesses /dev/mem, which has tight permissions.
    """
    args = {
        'delay': {
            'nargs': '?',
            'type': float,
            'default': 0.5,
            'help': 'Time, in seconds, between photos'
        },
        'sensor-gpio': {
            'nargs': '?',
            'type': int,
            'default': 4,
            'help': 'GPIO connection sensor is connected to.'
        }
    }

    def __init__(self, camera, album, delay, sensor_gpio):
        """Passive Infrared Watch Constructor.

        Args:
            camera (PiCamera): camera object.
            album (str): Path to directory to store pictures in.
            delay (float): Time in seconds to wait between pictures.
            sensor_gpio (int): GPIO connection sensor is connected to.
        """
        _log.debug('%s.__init__()', self.__class__.__name__)

        super().__init__(camera, album)
        self._delay = delay
        self._sensor = sensor_gpio
        self._state = None

    def watch(self):
        _log.debug('%s.watch()', self.__class__.__name__)

        self._setup()

        try:
            self._watch_loop()

        finally:
            self._teardown()

    def _setup(self):
        _log.debug('%s._setup()', self.__class__.__name__)

        gpio.setmode(gpio.BCM)
        gpio.setup(self._sensor, gpio.IN, pull_up_down=gpio.PUD_DOWN)

    def _teardown(self):
        _log.debug('%s._teardown()', self.__class__.__name__)

        gpio.cleanup()

    def _watch_loop(self):
        """Infinite loop for picture taking.

        Picture taking is a two-state state machine:

        +------+ sensor high  +------------+
        | wait |------------->| photograph |--+ delay elapsed:
        |      |<-------------|            |<-+ take picture
        +------+   sensor low +------------+
        """
        _log.debug('%s._watch_loop()', self.__class__.__name__)

        self._state = self._wait_state

        while True:
            self._state()

    def _wait_state(self):
        """Wait state."""
        _log.debug('Entering wait state.')

        gpio.wait_for_edge(self._sensor, gpio.RISING)
        gpio.remove_event_detect(self._sensor)
        self._state = self._photograph_state

    def _photograph_state(self):
        """Photograph state."""
        _log.debug('Entering photograph state.')
        gpio.add_event_detect(self._sensor, gpio.FALLING)

        while True:
            capture_time = datetime.datetime.now()
            self._capture()
            if gpio.event_detected(self._sensor):
                gpio.remove_event_detect(self._sensor)
                self._state = self._wait_state
                break
            else:
                process_time = (
                    datetime.datetime.now() - capture_time
                ).total_seconds()
                if process_time < self._delay:
                    time.sleep(self._delay - process_time)
