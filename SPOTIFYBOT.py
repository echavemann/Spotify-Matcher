import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

SPOTIPY_CLIENT_ID = 'ee88aca00bc74b3d833b4899198f62c8'
SPOTIPY_CLIENT_SECRET = 'e1c12da7cb384f0985c57831d1bfff7a'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090'
SCOPE = 'user-top-read'
print("error message")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
client_secret=SPOTIPY_CLIENT_SECRET, show_dialog = True, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))


top_tracks_short = sp.current_user_top_tracks(limit = 50, offset = 0, time_range="short_term")
# print(top_tracks_short)

def get_track_ids(list):
    track_ids = []
    for song in list['items']:
        track_ids.append(song['id'])
    return track_ids

track_ids = get_track_ids(top_tracks_short)

def get_track_features(id):
    meta = sp.track(id)
    # meta is a dict with track info
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    spotify_url = meta['external_urls']['spotify']
    album_cover = meta['album']['images'][0]['url']
    track_info = [name, album, artist, spotify_url, album_cover]
    return track_info

for track in track_ids:
    print(get_track_features(track)[0])

