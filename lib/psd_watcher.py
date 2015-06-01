"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
from lib.albatross import log
from lib.watcher import Watcher

_log = log.get_logger(__name__)


class PsdWatcher(Watcher):
    """Power Spectral Density Watcher.

    Watcher that determines whether to take a picture based on deltas in the
    power spectral density of a picture and the mean of the 'no subjects'
    pictures.
    """
    def __init__(self, camera, album):
        _log.debug('%s.__init__()', self.__class__.__name__)

        super().__init__(camera, album)
        self._psd = None

    def watch(self):
        _log.debug('%s.watch()', self.__class__.__name__)

        while True:
            photo = self._capture()
