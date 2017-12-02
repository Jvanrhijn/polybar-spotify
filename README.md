# polybar-spotify

---

This is a module that shows the current song playing and its primary artist on Spotify, with a Spotify-green underline, for people that don't want to set up mpd. If Spotify is not active, nothing is shown. If the song name is longer than `trunclen` characers (default 25), it is truncated and `...` is appended. If the song is truncated and contains a single opening parenthesis, the closing paranethsis is appended as well.

This module requires python 3.x and the `dbus` module.

[![sample screenshot](https://i.imgur.com/kEluTSq.png)](https://i.imgur.com/kEluTSq.png)

### Settings
~~~ ini
[module/spotify]
type = custom/script
interval = 1
format-prefix = " "
format = <label>
exec = /path/to/spotify/script

format-underline = #1db954
