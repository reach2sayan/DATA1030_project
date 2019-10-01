import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt 
from sklearn.preprocessing import MinMaxScaler

def extract_date(df,column):
    df[column+"_year"] = df[column].dt.year
    df[column+"_month"] = df[column].dt.month
    df[column+"_day"] = df[column].dt.day
    #df = df.drop(df['date'])
    return df

path_to_data = "/home/sayan/Documents/Data Science/DATA1030/project/data"


#----------------------------------------------------------------------
# Pre Process albums database
#----------------------------------------------------------------------

df_albums = pd.read_csv(path_to_data+"/albums.csv")
df_albums = df_albums.dropna() #drop all rows with NaN values

#rename date to week of chart
df_albums = df_albums.rename(columns={'date':'date_on_chart'})

#parse dates to year,day and month
df_albums['date_on_chart'] = pd.to_datetime(df_albums['date_on_chart'])
df_albums = extract_date(df_albums,'date_on_chart')

#drop the id column
df_albums = df_albums.drop(['id'],axis=1)


#applying MinMax scaling to track_length
scaler = MinMaxScaler()
tl_values = scaler.fit_transform(df_albums['track_length'].values.reshape(-1,1))
df_albums['scaled_track_length'] = tl_values

#applying MinMax scaling to length
al_values = scaler.fit_transform(df_albums['length'].values.reshape(-1,1))
df_albums['scaled_length'] = al_values

#applying MinMax scaling to rank
rank_values = scaler.fit_transform(df_albums['rank'].values.reshape(-1,1))
df_albums['scaled_rank'] = rank_values

#--------------------------------------------------------------------
# pre process acoustic feature database
#--------------------------------------------------------------------

df_acoustic = pd.read_csv(path_to_data+"/acoustic_features.csv")
df_acoustic = df_acoustic.dropna() #drop all rows with NaN values

#applying MinMax scaling to song duration
dur_values = scaler.fit_transform(df_acoustic['duration_ms'].values.reshape(-1,1))
df_acoustic['scaled_duration'] = dur_values

#applying MinMax scaling to key 
key_values = scaler.fit_transform(df_acoustic['key'].values.reshape(-1,1))
df_acoustic['scaled_key'] = key_values

#applying MinMax scaling to tempo
tempo_values = scaler.fit_transform(df_acoustic['tempo'].values.reshape(-1,1))
df_acoustic['scaled_tempo'] = tempo_values

#applying MinMax scaling to time_signature
time_values = scaler.fit_transform(df_acoustic['time_signature'].values.reshape(-1,1))
df_acoustic['scaled_time_signature'] = time_values

#applying MinMax scaling to loudness
ld_values = scaler.fit_transform(df_acoustic['loudness'].values.reshape(-1,1))
df_acoustic['scaled_loudness'] = ld_values

#rename date to date_release
df_acoustic = df_acoustic.rename(columns={'date':'date_release'})
df_acoustic['date_release'] = pd.to_datetime(df_acoustic['date_release'])
df_acoustic = extract_date(df_acoustic,'date_release')

#rename id to song_id
df_acoustic = df_acoustic.rename(columns={'id':'song_id'})

#drop redundant columns and create new_preprocessed csv
merged_df = pd.merge(df_acoustic,df_albums, on=['album','artist'],how='inner')
merged_df = merged_df.drop(['song','album','artist','duration_ms','track_length','date_on_chart','date_release','date_on_chart','loudness','rank','length','key','tempo','time_signature'],axis=1)
merged_df.to_csv(path_to_data+"/data_pp.csv")
