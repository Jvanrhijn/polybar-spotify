#!/bin/python

import sys
import dbus
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--trunclen', type=int, metavar='trunclen')
args = parser.parse_args()

if args.trunclen is not None:
    trunclen = args.trunclen
else:
    trunclen = 25

try:
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")

    spotify_properties = dbus.Interface(spotify_bus, "org.freedesktop.DBus.Properties")

    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    artist = metadata['xesam:artist'][0]
    song = metadata['xesam:title']

    if len(song) > trunclen:
        song = song[0:trunclen]
        song += '...' 
        if ('(' in song) and (')' not in song):
            song += ')'
    output = artist + ': ' + song
    
    # Python3 uses UTF-8 by default. 
    if sys.version_info.major == 3:
        print(output)
    else:
        print(output.encode('UTF-8'))
except Exception as e:
    if isinstance(e, dbus.exceptions.DBusException):
        print("")
    else:
        print(e)
