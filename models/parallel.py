
import os
from tqdm import tqdm
from concurrent.futures import as_completed, ProcessPoolExecutor
import pandas as pd

# function to apply to a small section


def someFunc(df, arg1, arg2):
    pass


# pool setup
pool_size = os.cpu_count() - 8
executor = ProcessPoolExecutor(max_workers=pool_size)


# break it up, put in list
listGroupDF = list(mainDF.groupby(["ColVal"]))

# submit jobs and put in a list
arg1 = 'theArgs'
jobs = [
    executor.submit(someFunc, arg1, someIdx)
    for someIdx, df in listGroupDF
]

split_df = []
for job in tqdm(as_completed(jobs), total=len(jobs), desc="What  it doing"):
    split_df.append(job.result())

# aggreage at the end
outDF = pd.concat(split_df, ignore_index=True)
