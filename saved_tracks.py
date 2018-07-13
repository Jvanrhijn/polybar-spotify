from __future__ import print_function
import os
import sys
import time
import json
import spotipy
import spotipy.oauth2

if sys.version_info.major >= 3:
    import configparser
    WRITE_MODE = 'w'
else:
    import ConfigParser as configparser
    WRITE_MOD = 'wb'

PREFS_FILE = os.environ['HOME'] + '/.config/spotify/barconfig.cfg'
REDIRECT_URI = 'http://localhost'
SCOPE = 'user-library-read user-library-modify '

# Parse all config under the "authorization" header
SECTION = 'authorization'
prefs = configparser.RawConfigParser()
prefs.readfp(open(PREFS_FILE))

# Check whether to use the cached value
def get_track_cache(track):
    try:
        cached = json.loads(prefs.get(SECTION, 'cache'))
        if time.time() - cached['time'] < 20 and cached['track'] == track:
            return cached['saved']
        return None
    except:
        return None

def save_track_cache(track, val):
    prefs.set(SECTION, 'cache', json.dumps({ 'time': time.time(), 'saved': val, 'track': track }))
    with open(PREFS_FILE, WRITE_MODE) as f:
        prefs.write(f)
    
def get_client():
    # Either retrieve the token from the config file, or if not present get one from Spotify
    client_id = prefs.get(SECTION, 'client_id')
    client_secret = prefs.get(SECTION, 'client_secret')
    oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, REDIRECT_URI, scope=SCOPE)
    try:
        token_info = json.loads(prefs.get(SECTION, 'token'))
        if token_info['expires_at'] - time.time() < 60:
            token_info = oauth.refresh_access_token(token_info['refresh_token'])
    except configparser.NoOptionError:
        print('''
             User authentication requires interaction with your
             web browser. Once you enter your credentials and
             give authorization, you will be redirected to
             a url.  Paste that url you were directed to to
             complete the authorization.
        ''')
        auth_url = oauth.get_authorize_url()
        try:
            import webbrowser
            webbrowser.open(auth_url)
            print('Opening %s in your browser' % auth_url)
        except:
            print('Please navigate here: %s' % auth_url)
        print('\n')
        try:
            response = raw_input('Enter the URL you were redirected to: ')
        except NameError:
            response = input('Enter the URL you were redirected to: ')
        print('\n')
        code = oauth.parse_response_code(response)
        token_info = oauth.get_access_token(code)

        print(token_info)
        prefs.set(SECTION, 'token', json.dumps(token_info))
        with open(PREFS_FILE, WRITE_MODE) as f:
            prefs.write(f)  

    # Create the Spotify client
    return spotipy.Spotify(auth=token_info['access_token'])

def track_saved(track):
    if 'spotify.com/ad' in track:
        return False
    saved_by_cache = get_track_cache(track)
    if saved_by_cache is not None:
        return saved_by_cache
    sp = get_client()
    val = sp.current_user_saved_tracks_contains([track])[0]
    save_track_cache(track, val)
    return val

def save_track(track):
    sp = get_client()
    if track_saved(track):
        sp.current_user_saved_tracks_delete([track])
        saved = False
    else:
        sp.current_user_saved_tracks_add([track])
        saved = True
    save_track_cache(track, saved)
