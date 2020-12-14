# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 23:12:09 2020
@author: AP
get data from json files
"""

import os
import re
import numpy as np
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def fetch_data(data_dir):
    """
    laod all json formatted files into a dataframe
    """

    # input testing
    if not os.path.isdir(data_dir):
        raise Exception("specified data dir does not exist")
    if not len(os.listdir(data_dir)) > 0:
        raise Exception("specified data dir does not contain any files")

    file_list = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if re.search("\.json", f)]
    correct_columns = ['country', 'customer_id', 'day', 'invoice', 'month',
                       'price', 'stream_id', 'times_viewed', 'year']

    # read data into a temp structure
    all_months = {}
    for file_name in file_list:
        df = pd.read_json(file_name)
        all_months[os.path.split(file_name)[-1]] = df

    # ensure the data are formatted with correct columns
    for f, df in all_months.items():
        cols = set(df.columns.tolist())
        if 'StreamID' in cols:
            df.rename(columns={'StreamID': 'stream_id'}, inplace=True)
        if 'TimesViewed' in cols:
            df.rename(columns={'TimesViewed': 'times_viewed'}, inplace=True)
        if 'total_price' in cols:
            df.rename(columns={'total_price': 'price'}, inplace=True)

        cols = df.columns.tolist()
        if sorted(cols) != correct_columns:
            raise Exception("columns name could not be matched to correct cols")

    # concat all of the data
    df = pd.concat(list(all_months.values()), sort=True)
    years, months, days = df['year'].values, df['month'].values, df['day'].values
    dates = ["{}-{}-{}".format(years[i], str(months[i]).zfill(2), str(days[i]).zfill(2)) for i in range(df.shape[0])]
    df['invoice_date'] = np.array(dates, dtype='datetime64[D]')
    df['invoice'] = [re.sub("\D+", "", i) for i in df['invoice'].values]

    # sort by date and reset the index
    df.sort_values(by='invoice_date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    return (df)


if __name__ == "__main__":
    run_start = time.time()
    input_data = "data\cs-train"
    data_dir = os.path.join("data", "cs-train")
    print(data_dir)
    all_data_df = fetch_data(data_dir)
    print(all_data_df.columns)
    print(all_data_df.head)
