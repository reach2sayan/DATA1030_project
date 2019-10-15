import pandas as pd
import numpy as np

path_to_data = "/home/sayan/Documents/Data Science/DATA1030/project/data"

df_albums = pd.read_csv(path_to_data+"/albums.csv")
df_albums = df_albums.dropna()
df_albums = df_albums.drop(columns=['id','rank','date'],axis=1)

df_acoustic = pd.read_csv(path_to_data+"/acoustic_features.csv")
df_acoustic = df_acoustic.dropna()
df_acoustic = df_acoustic.drop(columns='date',axis=1)

merged_df = pd.merge(df_acoustic,df_albums,on=['album','artist'],how='inner')

merged_df = merged_df.drop_duplicates(subset=None,keep='first',inplace=False).reset_index(drop=True)

merged_df = merged_df.drop(columns=['album','song','artist','track_length'],inplace=False)

merged_df['billboard'] = [1 for i in range(merged_df.shape[0])]
merged_df.to_csv(path_to_data+"/data_raw_1.csv")
