import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import datetime as dt
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor

path_to_data = "/home/sayan/Documents/Data Science/DATA1030/project/data"

def extract_date(df,column):
    df[column+"_year"] = df[column].dt.year
    df[column+"_month"] = df[column].dt.month
    df[column+"_day"] = df[column].dt.day
    #df = df.drop(df['date'])
    return df

df = pd.read_csv(path_to_data+"/data_raw_final.csv")

#df_acoustic['date'] = pd.to_datetime(df_acoustic['date'])
df['date'] = pd.to_datetime(df['date'])
df = extract_date(df,'date')

dec = df['date_year'].values - (df['date_year'].values)%10 

df['decade'] = dec
df.to_csv(path_to_data+"/data_raw_final_date_separated.csv",index=False)
cont_ftrs = ['track_length','length','key','duration_ms', 'tempo', 'time_signature', 'loudness','date_year','date_month','date_day','decade']

le = LabelEncoder()

numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, cont_ftrs)])
X_prep = preprocessor.fit_transform(df)

feature_names = preprocessor.transformers_[0][-1]

df_pp = pd.DataFrame(data=X_prep,columns=feature_names)
df_pp['acousticness'] = df['acousticness'].values
df_pp['speechiness'] = df['speechiness'].values
df_pp['instrumentalness'] = df['instrumentalness'].values
df_pp['danceability'] = df['danceability'].values
df_pp['valence'] = df['valence'].values
df_pp['liveness'] = df['liveness'].values
df_pp['loudness'] = df['loudness'].values
df_pp['mode'] = df['mode'].values
df_pp['energy'] = df['energy'].values
df_pp['id'] = df['id'].values
df_pp['album_id'] = df['album_id'].values
#df_pp['decade'] = le.fit_transform(df['decade'])
df_pp['billboard'] = df['billboard'].values

cols = ['track_length', 'length', 'key', 'duration_ms', 'tempo',
       'time_signature', 'loudness', 'date_year', 'date_month', 'date_day', 'acousticness', 'speechiness', 'instrumentalness', 'danceability', 'valence', 'liveness', 'mode', 'energy', 'billboard']

imputer = IterativeImputer(estimator=RandomForestRegressor(),random_state=2000)
X = df_pp[cols].values
X_impute = imputer.fit_transform(X)

df_pp = df_pp.drop(['track_length'], axis=1)
df_pp['track_length'] = X_impute[:,0]

df_pp.to_csv(path_to_data+"/data_pp.csv",index=False)
