import pandas as pd
import numpy as np
import datetime as dt

path_to_data = "/home/sayan/Documents/Data Science/DATA1030/project/data"

def extract_date(df,column):
    df[column+"_year"] = df[column].dt.year
    df[column+"_month"] = df[column].dt.month
    df[column+"_day"] = df[column].dt.day
    #df = df.drop(df['date'])
    return df


df_albums = pd.read_csv(path_to_data+"/albums.csv")
df_albums = df_albums.dropna()
df_albums = df_albums.drop(columns=['id','rank','date'],axis=1)

df_acoustic = pd.read_csv(path_to_data+"/acoustic_features.csv")
df_acoustic = df_acoustic.dropna()
#df_acoustic = df_acoustic.drop(columns='date',axis=1)
#df_acoustic['date'] = pd.to_datetime(df_acoustic['date'])
#df_acoustic = extract_date(df_acoustic,'date')



merged_df = pd.merge(df_acoustic,df_albums,on=['album','artist'],how='inner')

merged_df = merged_df.drop_duplicates(subset=None,keep='first',inplace=False).reset_index(drop=True)

merged_df = merged_df.drop(columns=['album','song','artist'],inplace=False)

#dec = []
#for i in range(merged_df.shape[0]):
    #dec.append(merged_df['date_year'][i]-(merged_df['date_year'][i]%10))
    
#merged_df['decade'] = dec
merged_df['billboard'] = [1 for i in range(merged_df.shape[0])]
merged_df.to_csv(path_to_data+"/data_raw.csv", index=False)
