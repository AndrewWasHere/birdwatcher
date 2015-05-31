"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import argparse
import datetime
import picamera
from lib.albatross import log
from lib.albatross.path import abs_path
from lib.psd_watcher import PsdWatcher

_log = log.get_logger(__name__)


def parse_command_line():
    parser = argparse.ArgumentParser()

    parser = log.add_log_parser_arguments(parser)

    # Photo album settings
    parser.add_argument('--album', nargs='?', default='/tmp/photos')

    # Camera settings
    parser.add_argument('--vflip', action='store_true')
    parser.add_argument('--hflip', action='store_true')

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
        watcher = PsdWatcher(camera, args.album)
        watcher.watch()


if __name__ == '__main__':
    main()
