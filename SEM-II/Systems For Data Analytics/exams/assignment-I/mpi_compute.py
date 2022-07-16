from mpi4py import MPI
import pandas as pd
from worker import *
from tabulate import tabulate

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

local_results = process_data(rank)

if rank > 0:
    print("Sending results for worker ", rank, " :", local_results)
    comm.send(local_results, dest=0, tag = 14)
else:
    print("Sending results for worker ", rank, " :", local_results)
    accumulated_profits = local_results["profits"]
    total_items = local_results["items"]
    df = pd.read_pickle('sum{}.pkl'.format(rank + 1))
    for i in range(1,size):
        worker_results = comm.recv(source=i,tag=14)
        accumulated_profits += worker_results["profits"]
        total_items += worker_results["items"]
        df_i = pd.read_pickle('sum{}.pkl'.format(i + 1))
        df = pd.concat([df,df_i])
    df = df.groupby('region').sum()
    print('Ans 1: Total \'units_sold\' in each region \n')
    print(df.to_markdown(tablefmt='pretty',stralign='left'))
    print('\n')
    print('Ans 2: Average \'total_profit\' per transaction: ',round(accumulated_profits/total_items,2))
