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

df_albums = pd.read_csv(path_to_data+"/albums.csv")
df_albums = df_albums.dropna() #drop all rows with NaN values


#parse dates to year,day and month
df_albums['date'] = pd.to_datetime(df_albums['date'])
df_albums = extract_date(df_albums,'date')


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

#drop redundant columns and create new pre-processed csv
df_albums = df_albums.drop(['rank','length','date','track_length'],axis=1)

df_albums.to_csv(path_to_data+"/albums_pp.csv")
