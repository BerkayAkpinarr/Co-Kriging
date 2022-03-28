import pandas as pd
import numpy as np
from statistical_methods import calculate_md, calculate_kge, calculate_nrmse


def read_csv(path):
    df = pd.read_csv(path)
    return df


def calculate_statistics_all(cmip6, era5):
    pearson_r = np.corrcoef(cmip6, era5)[0, 1]
    nrmse = calculate_nrmse(cmip6, era5)
    md = calculate_md(cmip6, era5)
    kge = calculate_kge(cmip6, era5)
    a = 1
    return md, nrmse, pearson_r, kge


data_path = r"./results/access-cm-2.csv"

df = read_csv(data_path)

grid_list = np.unique(df.id.to_numpy())

cmip6_value = df['cmip6_values'].to_numpy()
min_era5 = df['min_era5'].to_numpy()
max_era5 = df['max_era5'].to_numpy()
mean_era5 = df['mean_era5'].to_numpy()
median_era5 = df['median_era5'].to_numpy()
observation_list = [min_era5, max_era5, mean_era5, median_era5]
value_type_list = ['min', 'max', 'mean', 'median']

for value_type, era5_value in zip(value_type_list, observation_list):
    print(f"Results for {value_type}:")
    grid_md, grid_nrmse, grid_pearson_r, grid_kge = calculate_statistics_all(cmip6_value, era5_value)
    print(f'md: {grid_md} nrmse: {grid_nrmse} pearson_r: {grid_pearson_r} kge: {grid_kge}')
    a = 1

# for grid_id in grid_list:
#     new_df = df.loc[df.id == grid_id, :]
#     cmip6_value = new_df['cmip6_values'].to_numpy()
#     min_era5 = new_df['min_era5'].to_numpy()
#     max_era5 = new_df['max_era5'].to_numpy()
#     mean_era5 = new_df['mean_era5'].to_numpy()
#     median_era5 = new_df['median_era5'].to_numpy()
#     observation_list = [min_era5, max_era5, mean_era5, median_era5]
#     value_type_list = ['min', 'max', 'mean', 'median']
#     for value_type, era5_value in zip(value_type_list, observation_list):
#         print(f"Grid No: {grid_id}")
#         print(f"Results for {value_type}:")
#         grid_md, grid_nrmse, grid_pearson_r, grid_kge = calculate_statistics_all(cmip6_value, era5_value)
#         print(f'md: {grid_md} nrmse: {grid_nrmse} pearson_r: {grid_pearson_r} kge: {grid_kge}')