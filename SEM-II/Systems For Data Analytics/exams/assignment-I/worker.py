import pandas as pd
import time

def process_data(rank):
    df = pd.read_pickle('data_{}.pkl'.format(rank + 1))
    group_df = df.groupby('region')
    group_df['units_sold'].sum().to_pickle('sum{}.pkl'.format(rank +1))
    profit = df['total_profit'].sum()
    items = len(df)
    result = {'profits':round(profit,2),'items':items}
    return result


