"""
Copyright 2015 Andrew Lin.
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>. 
"""
import time
from lib.albatross import log
from lib.watcher import Watcher

_log = log.get_logger(__name__)


class NaiveWatcher(Watcher):
    """Naive Watcher.

    Watcher that just takes a picture every 'delay' seconds.
    """
    def __init__(self, camera, album, delay):
        """Naive Watcher Constructor

        Args:
            camera (PiCamera): camera object.
            album (str): Path to directory to store pictures in.
            delay (float): Time in seconds to wait between pictures
        """
        _log.debug('%s.__init__()', self.__class__.__name__)

        super().__init__(camera, album)
        self._delay = delay

    def watch(self):
        _log.debug('%s.watch()', self.__class__.__name__)

        while True:
            photo = self._capture()
            time.sleep(self._delay)
