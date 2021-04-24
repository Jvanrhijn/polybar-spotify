#!/bin/bash

# initialize polybar-spotify scroll if the process exists
PLAYER=$(playerctl metadata --format '{{playerName}}' 2>&1)
if [ "$PLAYER" = "spotify" ]; then
    python -u /path/to/spotify/script -s -t 35 -f '{artist}: {song}' -p '[playing],[paused]'
fi

