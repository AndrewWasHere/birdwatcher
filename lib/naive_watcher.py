"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>. 
"""
import time
import datetime
from lib.albatross import log
from lib.watcher import Watcher

_log = log.get_logger(__name__)


class NaiveWatcher(Watcher):
    """Naive Watcher.

    Watcher that just takes a picture every 'delay' seconds.
    """
    # Camera and album are assumed to be handled by the calling module.
    args = {
        'delay': {
            'nargs': '?',
            'type': float,
            'default': 10,
            'help': 'Time, in seconds, between photos'
        },
        'duration': {
            'nargs': '?',
            'type': float,
            'default': None,
            'help': 'Time, in seconds, for program to run. '
                    'If not specified, run forever'
        }
    }

    def __init__(self, camera, album, delay, duration):
        """Naive Watcher Constructor.

        Args:
            camera (PiCamera): camera object.
            album (str): Path to directory to store pictures in.
            delay (float): Time in seconds to wait between pictures.
            duration (float): Time in seconds to run. None or 0 => Don't stop.
        """
        _log.debug('%s.__init__()', self.__class__.__name__)

        super().__init__(camera, album)
        self._delay = delay
        self._duration = duration

    def watch(self):
        _log.debug('%s.watch()', self.__class__.__name__)

        start_time = datetime.datetime.now()
        end_time = (
            start_time + datetime.timedelta(seconds=self._duration)
            if self._duration else
            None
        )

        while not end_time or datetime.datetime.now() < end_time:
            self._capture()
            time.sleep(self._delay)
