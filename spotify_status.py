#!/usr/bin/env python

import sys
import dbus
import argparse
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

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
    '-p',
    '--playpause',
    type=str,
    metavar='play-pause indicator',
    dest='play_pause'
)
parser.add_argument(
    '--font',
    type=str,
    metavar='the index of the font to use for the main label',
    dest='font'
)
parser.add_argument(
    '--playpause-font',
    type=str,
    metavar='the index of the font to use to display the playpause indicator',
    dest='play_pause_font'
)
parser.add_argument(
    '-q',
    '--quiet',
    action='store_true',
    help="if set, don't show any output when the current song is paused",
    dest='quiet',
)

args = parser.parse_args()


def fix_string(string):
    # corrects encoding for the python version used
    if sys.version_info.major == 3:
        return string
    else:
        return string.encode('utf-8')


def truncate(name, trunclen):
    if len(name) > trunclen:
        name = name[:trunclen]
        name += '...'
        if ('(' in name) and (')' not in name):
            name += ')'
    return name



# Default parameters
output = fix_string(u'{play_pause} {artist}: {song}')
trunclen = 35
play_pause = fix_string(u'\u25B6,\u23F8') # first character is play, second is paused

label_with_font = '%{{T{font}}}{label}%{{T-}}'
font = args.font
play_pause_font = args.play_pause_font

quiet = args.quiet

# parameters can be overwritten by args
if args.trunclen is not None:
    trunclen = args.trunclen
if args.custom_format is not None:
    output = args.custom_format
if args.play_pause is not None:
    play_pause = args.play_pause

play_pause_icons = play_pause.split(',')

last_metadata = None
last_status = None

def query_and_print():
    global bus
    try:
        spotify_bus = bus.get_object(bus_name='org.mpris.MediaPlayer2.spotify',
                                     object_path='/org/mpris/MediaPlayer2')
        spotify_properties = dbus.Interface(spotify_bus,
                                            dbus_interface='org.freedesktop.DBus.Properties')
        metadata = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
        status = spotify_properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')

        print_output(metadata, status)
    except:
        print('', flush=True)

def print_output(metadata, status):
    global play_pause_icons
    global play_pause_font
    global last_metadata
    global last_status

    last_metadata = metadata
    last_status = status

    # Handle play/pause label

    if status == 'Playing':
        play_pause = play_pause_icons[0]
    elif status == 'Paused':
        play_pause = play_pause_icons[1]
    else:
        play_pause = str()

    if play_pause_font:
        play_pause = label_with_font.format(font=play_pause_font, label=play_pause)

    # Handle main label

    artist = fix_string(metadata['xesam:artist'][0]) if metadata['xesam:artist'] else ''
    song = fix_string(metadata['xesam:title']) if metadata['xesam:title'] else ''
    album = fix_string(metadata['xesam:album']) if metadata['xesam:album'] else ''

    if quiet and status == 'Paused':
        print('', flush=True)
    elif not artist and not song:
        query_and_print()
    else:
        if font:
            artist = label_with_font.format(font=font, label=artist)
            song = label_with_font.format(font=font, label=song)
            album = label_with_font.format(font=font, label=album)

        # Add 4 to trunclen to account for status symbol, spaces, and other padding characters
        print(truncate(output.format(artist=artist,
                                     song=song,
                                     play_pause=play_pause,
                                     album=album), trunclen + 4), flush=True)

def signal_handler(*args, **kwargs):
    global last_metadata
    global last_status
    if args[0] == 'org.mpris.MediaPlayer2.Player':
        metadata = last_metadata
        status = last_status
        if 'Metadata' in args[1]:
            metadata = args[1]['Metadata']
        if 'PlaybackStatus' in args[1]:
            status = args[1]['PlaybackStatus']
        print_output(metadata, status)
    elif kwargs['sender'] == 'org.freedesktop.DBus' and args[0] == 'org.mpris.MediaPlayer2.spotify':
        # spotify terminated or started
        query_and_print()

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

# if spotify is running get initial song
query_and_print()

# spotify signal handler
bus.add_signal_receiver(signal_handler,
                        signal_name='PropertiesChanged',
                        dbus_interface='org.freedesktop.DBus.Properties',
                        bus_name='org.mpris.MediaPlayer2.spotify',
                        path='/org/mpris/MediaPlayer2')

# spotify signal handler for termination and starting
bus.add_signal_receiver(signal_handler,
                        signal_name='NameOwnerChanged',
                        dbus_interface='org.freedesktop.DBus',
                        bus_name='org.freedesktop.DBus',
                        path='/org/freedesktop/DBus',
                        sender_keyword='sender')

loop = GLib.MainLoop()
loop.run()
