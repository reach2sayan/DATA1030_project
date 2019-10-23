import os
import glob
import pandas as pd
os.chdir("/home/sayan/Documents/Data Science/DATA1030/project/data/combined_data")

extension = 'csv'
all_filenames = [i for i in glob.glob('data_raw_big_*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined_csv.to_csv( "data_raw_final.csv", index=False)
