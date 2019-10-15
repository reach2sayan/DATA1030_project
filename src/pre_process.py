import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

path_to_data = "/home/sayan/Documents/Data Science/DATA1030/project/data"

df = pd.read_csv(path_to_data+"/df_raw.csv")

cont_ftrs = ['track_length','length','key','duration_ms', 'tempo', 'time_signature', 'loudness']

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
df_pp['energy'] = merged_df['energy'].values
df_pp['id'] = df['id'].values
df_pp['album_id'] = df['album_id'].values
df_pp['billboard'] = df['billboard'].values
df_pp.to_csv(path_to_data+"/data_pp.csv")
