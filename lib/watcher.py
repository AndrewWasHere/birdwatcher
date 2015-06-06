"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
from abc import ABCMeta, abstractmethod
import datetime
import os
from lib.albatross import log

_log = log.get_logger(__name__)


class Watcher(metaclass=ABCMeta):
    """Watcher interface."""
    # Args should be overridden by derived classes. It's key:value format is
    #   <command line arg>: <add_argument keywords dict>
    # where
    #   <command line arg> is the string after the '--' in the first
    #     argument to parser.add_argument(...)
    #   <add_argument keywords dict> is the keyword arguments following
    #     <command line arg>
    args = {}

    def __init__(self, camera, album):
        _log.debug('%s.__init__()', self.__class__.__name__)

        self._camera = camera
        self._album = album

    @classmethod
    def add_command_line_args(cls, subparsers, cmd, help_str):
        """Builds command line arguments parser for watcher arguments.

        Args:
            subparsers (argparse.SubParser): Subparser collection to add to.
            cmd (str): Sub-command.
            help_str (str): Help string to pass to subparsers.add_parser(...)
        """
        _log.debug('%s.add_command_line_args()', cls.__name__)

        parser = subparsers.add_parser(cmd, help=help_str)
        parser.set_defaults(watcher=cls)
        for k, v in cls.args.items():
            parser.add_argument('--{}'.format(k), **v)

    @classmethod
    def build(cls, camera, album, ns):
        """Factory method.

        Args:
            camera (PiCamera): Camera object.
            album (str): Path to photo album.
            ns (argparse.Namespace): Command line arguments.

        Returns:
            watcher (cls): Derived watcher class.
        """
        _log.debug('%s.build()', cls.__name__)

        kwargs = cls._namespace_to_dict(ns)
        return cls(camera, album, **kwargs)

    @abstractmethod
    def watch(self):
        """Observer loop."""

    @classmethod
    def _namespace_to_dict(cls, ns):
        """Converts relevant attributes of an argparse.Namespace to a dict.

        Args:
            ns (argparse.Namespace)

        Returns:
            (dict)
        """
        return {
            k: getattr(ns, k)
            for k in cls.args
        }

    @staticmethod
    def _timestamp():
        _log.debug('Watcher.timestamp()')

        ts = datetime.datetime.now()
        return ts.strftime('%Y%m%d_%H%M%S')

    def _capture(self):
        """Take a picture."""
        photo = os.path.join(self._album, '{}.jpg'.format(self._timestamp()))

        _log.info('Taking picture, %s.', photo)

        self._camera.capture(photo)

        return photo
