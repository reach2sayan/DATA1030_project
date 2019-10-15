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

    
def get_artists(df,sp):
    ids = df['album_id']
    result = []
    for album in ids:
        search_str = 'spotify:album:'+album
        result.append(sp.album(search_str))
    artists = [result[i]['artists'][0].get('id') for i in range(len(result))]
    return artists

def get_related_artists(df,sp):
    artist_id = df['artist_id']
    related_artists = []
    for artist in artist_id:
        related_artists.append(sp.artist_related_artists(artist))

    ra = []
    for i in range(len(related_artists)):
        for j in range(len(related_artists[i].get('artists'))):
            ra.append(related_artists[i].get('artists')[j].get('id'))

    return np.unique(ra)

def get_top_tracks(related_artists,sp):
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

def get_album_length(new_songs,sp):
    albums = new_songs['album_id']
    l = []
    for item in albums:
        res = sp.album(item)
        l.append(res.get('total_tracks'))

    return l

def get_song_features(new_songs,sp):
    songs = new_songs['id'].values

    acousticness = []
    danceability = []
    energy = []
    instrumentalness = []
    key = []
    liveness = []
    loudness = []
    mode = []
    speechiness = []
    tempo = []
    time_signature = []
    valence = []
    
    for song in songs:
        res = sp.audio_features(song)
        acousticness.append(res[0].get('acousticness'))
        danceability.append(res[0].get('danceability'))
        energy.append(res[0].get('energy'))
        instrumentalness.append(res[0].get('instrumentalness'))
        key.append(res[0].get('key'))
        speechiness.append(res[0].get('speechiness'))
        loudness.append(res[0].get('loudness'))
        liveness.append(res[0].get('liveness'))
        tempo.append(res[0].get('tempo'))
        mode.append(res[0].get('mode'))
        time_signature.append(res[0].get('time_signature'))
        valence.append(res[0].get('valence'))

    new_songs['acousticness'] = acousticness
    new_songs['danceability'] = danceability
    new_songs['energy'] = energy
    new_songs['instrumentalness'] = instrumentalness
    new_songs['key'] = key
    new_songs['loudness'] = loudness
    new_songs['liveness'] = liveness
    new_songs['tempo'] = tempo
    new_songs['mode'] = mode
    new_songs['speechiness'] = speechiness
    new_songs['time_signature'] = time_signature
    new_songs['valence'] = valence

    return new_songs

path_to_data = "/home/sayan/Documents/Data Science/DATA1030/project/data"

df = pd.read_csv(path_to_data+'/data_raw_1.csv')
df.drop(columns='Unnamed: 0',inplace=True)

sp = authorize_client()

df['artist_id'] = get_artists(df,sp)

related_artists = get_related_artists(df,sp)
new_songs = get_top_tracks(related_artists,sp)
new_songs['length'] = get_album_length(new_songs,sp)
new_songs = get_song_features(new_songs,sp)
new_songs['billboard'] = np.nan
df_big = pd.concat([df,new_songs],axis=0,ignore_index=True)
df_big = df_big.drop_duplicates('id', keep='first')
df_big['billboard'].fillna(0,inplace=True)

df_big.to_csv(path_to_data+'/data_raw_big.csv')
remove_cache()


