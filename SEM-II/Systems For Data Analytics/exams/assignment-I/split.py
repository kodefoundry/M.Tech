import pandas as pd
import numpy as np
import os
from filesplit.split import Split
import glob

# Define number of workers available, this can be passed a commandline also
# For the scope of this assignment it's kept hardcoded
no_workers = 4

size = os.path.getsize('geosales.csv')
chunk_size = size/4

split = Split('geosales.csv', './')
split.bysize(chunk_size,True,True)
files = glob.glob('geosales_*.csv')
files.sort()

last_file_id = len(files)
last_df = pd.DataFrame(columns=['region','units_sold','total_profit'])
for i,file in enumerate(files, start=1):
    df = pd.read_csv(file)[['region','units_sold','total_profit']]
    if i < 4:
        # Pickle file 1 - 3 directly
        df.to_pickle('data_{}.pkl'.format(i))
        os.remove(file)
    else:
        last_df = pd.concat([last_df,df])
        os.remove(file)
        if i == last_file_id:
            # 4 th chunk will be larger containing all data after 3rd chunk
            last_df.to_pickle('data_4.pkl'.format(i))
