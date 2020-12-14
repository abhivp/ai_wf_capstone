import pandas as pd
import matplotlib.pyplot as plt
from cslib import fetch_data

import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

base_dir = Path(__file__).parent
DATA_DIR = Path(base_dir / "data" / "cs-train").resolve()

pd.pandas.set_option('display.max_columns', None)
plt.style.use('seaborn')

SMALL_SIZE = 12
MEDIUM_SIZE = 14
LARGE_SIZE = 16

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=LARGE_SIZE)  # fontsize of the figure title

all_data_df = fetch_data(DATA_DIR)

print(f"List of Columns in data - {all_data_df.columns}")
print("Shape of Dataframe - Rows {} and Columns {}".format(all_data_df.shape[0], all_data_df.shape[1]))
print(all_data_df.head)

print("Count of Countries in the data - {}".format(len(pd.unique(all_data_df["country"]))))
print("List of Countries in the data - {}".format(all_data_df.country.unique()))

# missing values summary
print("Missing Value Summary\n{}".format("-" * 35))
print(all_data_df.isnull().sum(axis=0))

print("list of the variables that contain missing values")
vars_with_na = [var for var in all_data_df.columns if all_data_df[var].isnull().sum() > 0]
print(vars_with_na)
print("percentage of missing values")
print(all_data_df[vars_with_na].isnull().mean())

num_vars = [var for var in all_data_df.columns if all_data_df[var].dtypes != 'O']
print('Number of numerical variables: ', len(num_vars))
print(all_data_df[num_vars].head())

print(f"Transaction Date Range {all_data_df['invoice_date'].min()} to {all_data_df['invoice_date'].max()}")
print(f"Price Range {all_data_df['price'].min()} to {all_data_df['price'].max()}")

# Top 5 Countries by Revenue
revenue_by_cnt_df = all_data_df.groupby('country', as_index=False)['price']. \
    sum().dropna().sort_values('price', ascending=False)
print("Top 5 Countries by Revenue")
print(revenue_by_cnt_df.head(5))

print("Bottom 5 Countries by Revenue")
print(revenue_by_cnt_df.tail(5))

# Pivot summary
columns_to_show = ["price", "times_viewed"]
print(pd.pivot_table(all_data_df, index=['year', 'month'], values=columns_to_show, aggfunc='mean').round(3))

