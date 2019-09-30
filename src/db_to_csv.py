#code to separate databases from .db to .csv's

import pandas as pd
import sqlite3

cnx = sqlite3.connect('/home/sayan/Documents/Data Science/DATA1030/project/data/billboard-200.db')

df = pd.read_sql_query("SELECT * from albums", cnx)
df.to_csv(index=False,path_or_buf="../data/albums.csv")

df = pd.read_sql_query("SELECT * from acoustic_features", cnx)
df.to_csv(index=False,path_or_buf="../data/acoustic_features.csv")
