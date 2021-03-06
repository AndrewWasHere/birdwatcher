"""
Copyright 2015 Andrew Lin
All rights reserved.
Licensed under the BSD 3-clause License. See LICENSE.txt or
<http://opensource.org/licenses/BSD-3-Clause>.
"""
import argparse
import picamera
from lib.albatross import log
from lib.albatross.path import abs_path
from lib.naive_watcher import NaiveWatcher
from lib.pir_watcher import PirWatcher
from lib.psd_watcher import PsdWatcher

_log = log.get_logger(__name__)


def parse_command_line():
    parser = argparse.ArgumentParser()

    parser = log.add_log_parser_arguments(parser)

    # Photo album settings.
    parser.add_argument('--album', nargs='?', default='/tmp/photos')

    # Camera settings.
    parser.add_argument(
        '--vflip',
        action='store_true',
        help='Flip pictures vertically'
    )
    parser.add_argument(
        '--hflip',
        action='store_true',
        help='Flip pictures horizontally'
    )
    parser.add_argument(
        '--exposure-mode',
        nargs='?',
        default='sports',
        choices=picamera.PiCamera.EXPOSURE_MODES,
        help='Camera exposure modes'
    )

    # Watchers.
    subparsers = parser.add_subparsers()
    NaiveWatcher.add_command_line_args(
        subparsers,
        'naive',
        'Naive Watcher'
    )
    PsdWatcher.add_command_line_args(
        subparsers,
        'psd',
        'Power Spectral Density Watcher'
    )
    PirWatcher.add_command_line_args(
        subparsers,
        'pir',
        'Passive Infrared Watcher'
    )

    args = parser.parse_args()
    args.album = abs_path(args.album)

    return args


def configure_camera(camera, args):
    """Create and configure a picamera.

    Args:
        camera (picamera.PiCamera): camera to configure.
        args (argparse.Namespace): Command line arguments.

    Returns:
        camera (PiCamera): Configured camera.
    """
    _log.debug('configure_camera()')

    camera.vflip = args.vflip
    camera.hflip = args.hflip
    camera.exposure_mode = args.exposure_mode

    _log.info('Camera Settings:')
    _log.info('  hflip=%s', camera.hflip)
    _log.info('  vflip=%s', camera.vflip)
    _log.info('  exposure_mode=%s', camera.exposure_mode)

    return camera


def main():
    args = parse_command_line()

    with log.logger(**log.configure_logging(args)), \
        picamera.PiCamera(resolution=(2592, 1944)) as camera:

        configure_camera(camera, args)
        watcher = args.watcher.build(camera, args.album, args)
        watcher.watch()


if __name__ == '__main__':
    main()
