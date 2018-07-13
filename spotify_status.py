#!/bin/python

import sys
import dbus
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
    '-t',
    '--trunclen',
    type=int,
    metavar='trunclen'
)
parser.add_argument(
    '-f',
    '--format',
    type=str,
    metavar='custom format',
    dest='custom_format'
)
parser.add_argument(
    '-s',
    '--saved',
    type=str,
    metavar='saved icon',
    dest='saved_icon'
)
parser.add_argument(
    '-u',
    '--unsaved',
    type=str,
    metavar='unsaved icon',
    dest='unsaved_icon'
)
parser.add_argument('--save', dest='save_track', action='store_true')
args = parser.parse_args()

# Default parameters
output = '{artist}: {song}'
trunclen = 25

# parameters can be overwritten by args
if args.trunclen is not None:
    trunclen = args.trunclen
if args.custom_format is not None:
    output = args.custom_format

try:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object(
        'org.mpris.MediaPlayer2.spotify',
        '/org/mpris/MediaPlayer2'
    )

    spotify_properties = dbus.Interface(
        spotify_bus,
        'org.freedesktop.DBus.Properties'
    )

    metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')

    artist = metadata['xesam:artist'][0]
    song = metadata['xesam:title']
    if args.save_track:
        import saved_tracks
        saved_tracks.save_track(metadata['xesam:url'])
        sys.exit(0)

    if args.saved_icon:
        import saved_tracks
        saved = saved_tracks.track_saved(metadata['xesam:url'])
        saved_str = args.saved_icon if saved else ''
        unsaved_str = args.unsaved_icon if not saved else ''
    else:
        saved_str = ''
        unsaved_str = args.unsaved_icon

    if len(song) > trunclen:
        song = song[0:trunclen]
        song += '...'
        if ('(' in song) and (')' not in song):
            song += ')'

    # Python3 uses UTF-8 by default.
    if sys.version_info.major == 3:
        print(output.format(artist=artist, song=song, saved=saved_str, unsaved=unsaved_str))
    else:
        print(output.format(artist=artist, song=song, saved=saved_str, unsaved=unsaved_str).encode('UTF-8'))

except Exception as e:
    if isinstance(e, dbus.exceptions.DBusException):
        print('')
    else:
        print(e)
        print()
        import traceback
        traceback.print_exc()
