"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
from abc import ABCMeta, abstractclassmethod
import argparse
import picamera
from lib.albatross import log
from lib.albatross.path import abs_path
from lib.naive_watcher import NaiveWatcher
from lib.psd_watcher import PsdWatcher

_log = log.get_logger(__name__)


class WatcherFactory(metaclass=ABCMeta):
    """Watcher Factory."""
    # Args should be overridden by derived classes. It's key:value format is
    #   <command line arg>: <add_argument keywords dict>
    # where
    #   <command line arg> is the string after the '--' in the first
    #     argument to parser.add_argument(...)
    #   <add_argument keywords dict> is the keyword arguments following
    #     <command line arg>
    args = {}

    @classmethod
    def add_command_line_args(cls, subparsers, cmd, help_str):
        """Builds command line arguments parser for watcher arguments.

        Args:
            subparsers (argparse.SubParser): Subparser to add to.
            cmd (str): Sub-command.
            help_str (str): Help string to pass to subparsers.add_parser(...)
        """
        parser = subparsers.add_parser(cmd, help=help_str)
        parser.set_default(watcher_factory=cls)
        for k, v in cls.args.items():
            parser.add_argument('--{}'.format(k), **v)

    @classmethod
    def namespace_to_dict(cls, ns):
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

    @abstractclassmethod
    def build(cls, *_):
        """Build the watcher."""


class NaiveWatcherFactory(WatcherFactory):
    args = {
        'delay': {
            'nargs': '?',
            'type': float,
            'default': 10,
            'help': 'Time between photographs in seconds.'
        }
    }

    @classmethod
    def build(cls, camera, ns):
        kwargs = cls.namespace_to_dict(ns)
        return NaiveWatcher(camera, **kwargs)


class PsdWatcherFactory(WatcherFactory):
    args = {
        'delay': {
            'nargs': '?',
            'type': float,
            'default': 1,
            'help': 'Time between photographs in seconds.'
        }
    }

    @classmethod
    def build(cls, camera, ns):
        kwargs = cls.namespace_to_dict(ns)
        return PsdWatcher(camera, **kwargs)


def parse_command_line():
    parser = argparse.ArgumentParser()

    parser = log.add_log_parser_arguments(parser)

    # Photo album settings
    parser.add_argument('--album', nargs='?', default='/tmp/photos')

    # Camera settings
    parser.add_argument('--vflip', action='store_true')
    parser.add_argument('--hflip', action='store_true')

    # Watchers
    subparsers = parser.add_subparsers()
    NaiveWatcherFactory.add_command_line_args(
        subparsers,
        'naive',
        'Naive Watcher.'
    )
    PsdWatcherFactory.add_command_line_args(
        subparsers,
        'psd',
        'Power Spectral Density Watcher'
    )

    args = parser.parse_args()
    args.album = abs_path(args.album)

    return args


def configure_camera(args):
    """Create and configure a picamera.

    Args:
        args (argparse.Namespace): Command line arguments.

    Returns:
        camera (PiCamera): Configured camera.
    """
    _log.debug('configure_camera()')

    camera = picamera.PiCamera()
    camera.vflip = args.vflip
    camera.hflip = args.hflip

    _log.info('Camera Settings:')
    _log.info('  hflip=%s', camera.hflip)
    _log.info('  vflip=%s', camera.vflip)

    return camera


def main():
    args = parse_command_line()

    with log.logger(log.configure_logging(args)):
        camera = configure_camera(args)
        watcher = args.watcher_factory.build(camera, args)
        watcher.watch()


if __name__ == '__main__':
    main()
