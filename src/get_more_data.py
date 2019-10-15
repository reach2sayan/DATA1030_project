import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util
import os
import json
import pprint


def authorize_client():
    username = 'reach2sayan'
    CLIENT_ID = 'a55d8d9617de463cad7abce998314bb3'
    CLIENT_SECRET = '905ac33d383d47f6aca7cbb3f3c60d49'

    token = util.prompt_for_user_token(username, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://localhost/')

    sp = spotipy.Spotify(auth=token)
    return sp

def remove_cache():
    os.remove('.cache-reach2sayan')

    
def get_artists(df):
    ids = df['album_id']
    result = []
    for album in ids:
        search_str = 'spotify:album:'+album
        result.append(sp.album(search_str))
    artists = [result[i]['artists'][0].get('id') for i in range(len(result))]
    return artists

def get_related_artists(df):
    artist_id = df['artist_id']
    related_artists = []
    for artist in artist_id:
        related_artists.append(sp.artist_related_artists(artist))

    ra = []
    for i in range(len(related_artists)):
        for j in range(len(related_artists[i].get('artists'))):
            ra.append(related_artists[i].get('artists')[j].get('id'))

    return np.unique(ra)

def get_top_tracks(related_artists):
    duration_ms = []
    song = []
    album = []
    for artist in related_artists:
        res = sp.artist_top_tracks(artist_id=artist,country='US')
        for i in range(len(res)):
            duration_ms.append(res.get('tracks')[i].get('duration_ms'))
            song.append(res.get('tracks')[i].get('id'))
            alb = res.get('tracks')[i].get('album')['uri']
            alb = alb.replace('spotify:album:','')
            album.append(alb)

    new_songs = pd.DataFrame()
    new_songs['id'] = song
    new_songs['album_id'] = album
    new_songs['duration_ms'] = duration_ms

    new_songs = new_songs.drop_duplicates(subset=None,keep='first',inplace=False)

    return new_songs

def get_album_length(new_songs):
    albums = new_songs['album_id']
    l = []
    for item in albums:
        res = sp.album(item)
        l.append(res.get('total_tracks'))

    return l

def get_song_features(new_songs):
    

df = pd.read_csv('../data/data_raw_1_truncated.csv')
df.drop(columns='Unnamed: 0',inplace=True)

sp = authorize_client()

df['artist_id'] = get_artists(df)

related_artists = get_related_artists(df)
new_songs = get_top_tracks(related_artists)
l = get_album_length(new_songs)
new_songs['length'] = get_album_length(new_songs)

remove_cache()

