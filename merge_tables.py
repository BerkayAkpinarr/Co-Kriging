import os.path
import pathlib
import pandas as pd


def find_files(path):
    cmip6_list = []
    era5_list = []
    grid_table_list =[]
    for cmip6_table in pathlib.Path(path).glob('**/*_cmip6.csv'):
        cmip6_list.append(cmip6_table)
    for era5_table in pathlib.Path(path).glob('**/*_era5.csv'):
        era5_list.append(era5_table)
    for grid_table in pathlib.Path(path).glob('**/*_grid_table.csv'):
        grid_table_list.append(grid_table)
    return cmip6_list, era5_list, grid_table_list


def merge(cmip6, era5, grid):
    cmip6_df = pd.read_csv(cmip6)
    era5_df = pd.read_csv(era5)
    grid_df = pd.read_csv(grid)
    merged = pd.merge(cmip6_df, era5_df, on=['id', 'date'])
    merged_final = pd.merge(merged, grid_df, on=['id'])
    del cmip6_df, grid_df, era5_df
    print(f"done!")
    return merged_final


def export(merged_df):
    merged_df.to_csv(path_or_buf=r"./cnrm-esm2-1_bias_corrected_merged.csv", index=False)


input_path = r"./cnrm-esm2-1"
cmip6_csv_list, era5_csv_list, grid_csv_list = find_files(input_path)
for cmip6_csv, era5_csv, grid_csv in zip(cmip6_csv_list, era5_csv_list, grid_csv_list):
    merged = merge(cmip6_csv, era5_csv, grid_csv)
    export(merged)
