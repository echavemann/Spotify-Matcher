import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:9090'
SCOPE = 'user-top-read'

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

data = []

for track in track_ids:
    varList = []
    for attribute in get_track_features(track)[0:3]:
        varList.append(attribute)
    data.append(varList)

#Sheets Data
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

spreadsheetURL = '1c1qFAip2v4ih5Rdma5icaVI-pMka7sw-ovbSDd0NAfI'

service = build('sheets', 'v4', credentials=creds)

sheet = service.spreadsheets()


request = sheet.values().update(spreadsheetId=spreadsheetURL, range='Sheet1!B2', valueInputOption='USER_ENTERED', body={'values':data}).execute()
