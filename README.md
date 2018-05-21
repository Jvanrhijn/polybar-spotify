# polybar-spotify

This is a module that shows the current song playing and its primary artist on Spotify, with a Spotify-green underline, for people that don't want to set up mpd. If Spotify is not active, nothing is shown. If the song name is longer than `trunclen` characers (default 25), it is truncated and `...` is appended. If the song is truncated and contains a single opening parenthesis, the closing paranethsis is appended as well.

### Dependencies
- Python (2.x or 3.x)
- Python `dbus` module

[![sample screenshot](https://i.imgur.com/kEluTSq.png)](https://i.imgur.com/kEluTSq.png)

### Settings
~~~ ini
[module/spotify]
type = custom/script
interval = 1
format-prefix = " "
format = <label>
exec = python /path/to/spotify/script
format-underline = #1db954
~~~

#### Custom arguments

##### Truncate

The argument "-t" is optional and sets the `trunlen`. It specifies the maximum length of the song name, so that it gets truncated when the specified length is exceeded. Defaults to 25.

Override example:

~~~ ini
exec = python /path/to/spotify/script -t 42
~~~

##### Format

The argument "-f" is optional and sets the format. You can specify how to display the song and the artist's name. Useful if you want to swap the positions.

Override example:

~~~ ini
exec = python /path/to/spotify/script -f '{song} - {artist}'
~~~

This would output "Lone Digger - Caravan Palace" in your polybar, instead of what is shown in the screenshot.

