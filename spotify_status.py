#!/bin/python

import dbus
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--trunclen', type=int, metavar='trunclen')
args = parser.parse_args()

if hasattr(args, 'trunclen'):
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
    print(output.encode('utf-8'))
except Exception as e:
    print(e)
