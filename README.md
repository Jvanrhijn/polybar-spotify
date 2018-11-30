# polybar-spotify

This is a module that shows the current song playing and its primary artist on Spotify, with a Spotify-green underline, for people that don't want to set up mpd. If Spotify is not active, nothing is shown. If the song name is longer than `trunclen` characers (default 25), it is truncated and `...` is appended. If the song is truncated and contains a single opening parenthesis, the closing paranethsis is appended as well.

### Dependencies
- Python (2.x or 3.x)
- Python `dbus` module

[![sample screenshot](https://i.imgur.com/kEluTSq.png)](https://i.imgur.com/kEluTSq.png)

### Settings
``` ini
[module/spotify]
type = custom/script
interval = 1
format-prefix = " "
format = <label>
exec = python /path/to/spotify/script -f '{artist}: {song}'
format-underline = #1db954
```

#### Custom arguments

##### Truncate

The argument "-t" is optional and sets the `trunlen`. It specifies the maximum length of the song name, so that it gets truncated when the specified length is exceeded. Defaults to 25.

Override example:

``` ini
exec = python /path/to/spotify/script -t 42
```

##### Format

The argument "-f" is optional and sets the format. You can specify how to display the song and the artist's name, as well as where (or whether) to print the play-pause indicator. 

Override example:

``` ini
exec = python /path/to/spotify/script -f '{play_pause} {song} - {artist}'
```

This would output "Lone Digger - Caravan Palace" in your polybar, instead of what is shown in the screenshot.

##### Status indicator

The argument "-p" is optional, and sets which unicode symbols to use for the status indicator. These should be given as a comma-separated string, with the play indicator as the first value and the pause indicator as the second.

Override example:

``` ini
exec = python /path/to/spotify/script -p '[playing],[paused]'
```

##### Fonts

The argument "--font" is optional, and allow to specify which font from your Polybar config to use to display the main label.

Override example:
```ini
exec = python /path/to/spotify/script --font=1
```

The argument "--playpause-font" is optional, and allow to specify which font from your Polybar config to use to display the "play/pause" indicator.

Override example:
``` ini
exec = python /path/to/spotify/script -p '[playing],[paused]' --playpause-font=2
```
