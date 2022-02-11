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
SCOPE = 'user-top-read', 'user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
client_secret=SPOTIPY_CLIENT_SECRET, show_dialog = True, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

short_term_top_tracks = sp.current_user_top_tracks(limit = 50, offset = 0, time_range="short_term")
medium_term_top_tracks = sp.current_user_top_tracks(limit = 50, offset = 0, time_range="medium_term")
long_term_top_tracks = sp.current_user_top_tracks(limit = 50, offset = 0, time_range="long_term")

user_profile_name = sp.current_user()['display_name']
genre = sp.recommendation_genre_seeds()

def get_track_ids(list):
    track_ids = []
    for song in list['items']:
        track_ids.append(song['id'])
    return track_ids
short_term_track_ids = get_track_ids(short_term_top_tracks)
medium_term_track_ids = get_track_ids(medium_term_top_tracks)
long_term_track_ids = get_track_ids(long_term_top_tracks)

def get_track_features(id):
    meta = sp.track(id)
    # meta is a dict with track info
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    track_info = [name, album, artist]
    return track_info

header = [["Song Name", "Album", "Artist", '', "Song Name", "Album", "Artist", '', "Song Name", "Album", "Artist", '', "Top Genres"]]
short_term_data = []
medium_term_data = []
long_term_data = []
genres = []

for value in genre['genres']:
    temp = []
    temp.append(value)
    genres.append(temp)

for track in short_term_track_ids:
    varList = []
    for attribute in get_track_features(track):
        varList.append(attribute)
    short_term_data.append(varList)

for track in medium_term_track_ids:
    varList = []
    for attribute in get_track_features(track):
        varList.append(attribute)
    medium_term_data.append(varList)

for track in long_term_track_ids:
    varList = []
    for attribute in get_track_features(track):
        varList.append(attribute)
    long_term_data.append(varList)

#Sheets Data
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = ('key.json')

creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

spreadsheetURL = '1c1qFAip2v4ih5Rdma5icaVI-pMka7sw-ovbSDd0NAfI'

service = build('sheets', 'v4', credentials=creds)

try:
    new_sheet = {'requests': [
                {'addSheet':{'properties':{'title': user_profile_name}}}
                ]}

    res = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetURL, body=new_sheet).execute()
except:
    sheet = service.spreadsheets()
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetURL).execute()
    sheet_id = None
    for _sheet in spreadsheet['sheets']:
        if _sheet['properties']['title'] == user_profile_name:
            sheet_id = _sheet['properties']['sheetId']

    old_sheet = {'requests': [
                {'deleteSheet':{'sheetId':sheet_id}}
                ]}

    res = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetURL, body=old_sheet).execute()
    
    new_sheet = {'requests': [
                {'addSheet':{'properties':{'title': user_profile_name}}}
                ]}

    res1 = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetURL, body=new_sheet).execute()

sheet.values().update(spreadsheetId=spreadsheetURL, range=user_profile_name + '!A1', valueInputOption='USER_ENTERED', 
                                body={'values':header}).execute()

sheet.values().update(spreadsheetId=spreadsheetURL, range=user_profile_name + '!A2', valueInputOption='USER_ENTERED', 
                                body={'values':short_term_data}).execute()

sheet.values().update(spreadsheetId=spreadsheetURL, range=user_profile_name + '!E2', valueInputOption='USER_ENTERED', 
                                body={'values':medium_term_data}).execute()

sheet.values().update(spreadsheetId=spreadsheetURL, range=user_profile_name + '!I2', valueInputOption='USER_ENTERED', 
                                body={'values':long_term_data}).execute()

sheet.values().update(spreadsheetId=spreadsheetURL, range=user_profile_name + '!M2', valueInputOption='USER_ENTERED', 
                                body={'values':genres}).execute()
