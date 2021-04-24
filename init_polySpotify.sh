#!/bin/bash

# initialize polybar-spotify scroll if the process exists
PLAYER=$(playerctl metadata --format '{{playerName}}' 2>&1)
if [ "$PLAYER" = "spotify" ]; then
    python -u /home/henry/.config/polybar/scripts/polybar-spotify/spotify_status.py -s -t 35 -f '{artist}: {song}' -p ' , '
fi

