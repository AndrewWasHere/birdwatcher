"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
from abc import ABCMeta, abstractmethod
import datetime
from lib.albatross import log

_log = log.get_logger(__name__)


class Watcher(metaclass=ABCMeta):
    """Watcher interface."""
    def __init__(self, camera, album):
        _log.debug('%s.__init__()', self.__class__.__name__)

        self._camera = camera
        self._album = album

    @abstractmethod
    def watch(self):
        """Observer loop."""
        _log.error(
            '%s.watch() -- this should not happen!',
            self.__class__.__name__
        )

    @staticmethod
    def timestamp():
        _log.debug('Watcher.timestamp()')

        ts = datetime.datetime.now()
        return ts.strftime('%Y%m%d_%H%M%S')
