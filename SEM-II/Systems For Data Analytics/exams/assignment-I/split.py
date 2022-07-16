import pandas as pd
import numpy as np

# Define number of workers available, this can be passed a commandline also
# For the scope of this assignment it's kept hardcoded
no_workers = 4

# Read geosales.csv as a pandas DataFrame
df = pd.read_csv('geosales.csv')[['region','units_sold','total_profit']]

# Use numpy to split the data frames in to smaller dataframes to be pickled
df_chunks = np.array_split(df, no_workers)

# Split the dataframes into smaller data frames equal to number of available workers and pickle
for i,chunk in enumerate(df_chunks):
    out_path = 'data_{}.pkl'.format(i+1)
    chunk.to_pickle(out_path)

# Test code to check if pickling was correct and no data loss
# chunk_1_df = pd.read_pickle('assignment/data_1.pkl')
# chunk_1_df.size








