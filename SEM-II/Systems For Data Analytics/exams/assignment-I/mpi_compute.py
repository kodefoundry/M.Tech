from mpi4py import MPI
import pandas as pd
from worker import *
from tabulate import tabulate
import numpy as np

comm = MPI.COMM_WORLD

size = comm.Get_size()
rank = comm.Get_rank()

start_time = MPI.Wtime()
local_results = process_data(rank)
local_results["compute_time"] = MPI.Wtime() - start_time

if rank > 0:
    print("Process {}: Results form worker: {}".format(rank, local_results))
    comm.send(local_results, dest=0, tag = 14)
else:
    print("Process {}: Results form worker: {}".format(rank, local_results))
    accumulated_profits = local_results["profits"]
    total_items = local_results["items"]
    df = pd.read_pickle('sum{}.pkl'.format(rank + 1))
    for i in range(1,size):
        worker_results = comm.recv(source=i,tag=14)
        accumulated_profits += worker_results["profits"]
        total_items += worker_results["items"]
        df_i = pd.read_pickle('sum{}.pkl'.format(i + 1))
        df = pd.concat([df,df_i])
    print('Process {}: Total compute_time spent in server: {}\n'.format(rank,(MPI.Wtime()- start_time)))

    # Pretty printing queries results after computation in server
    df = df.groupby('region').sum()
    print('Process {}: Ans 1: Total \'units_sold\' in each region \n'.format(rank))
    print(df.to_markdown(tablefmt='pretty',stralign='left'))
    print('\n')
    print('Process {}: Ans 2: Average \'total_profit\' per transaction: {}\n'.format(rank,round(accumulated_profits/total_items,2)))
