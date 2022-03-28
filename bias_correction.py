import os
import pandas as pd
from playground import read_file, convert_monthly_yearly_mean, convert_monthly_yearly_sum
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'


def linear_correction():
    data_path = r"./results/access-cm-2.csv"

    data = read_file(data_path)
    grid_list = np.unique(data.id.to_numpy())
    new_data = []

    for grid in grid_list:
        grid_data_daily = data.loc[data.id == grid, :]
        grid_data_daily['date'] = pd.to_datetime(grid_data_daily['date'], format='%Y-%m-%d %H:%M:%S')
        grid_data_daily.set_index('date', inplace=True)
        grid_data_monthly, grid_data_yearly = convert_monthly_yearly_sum(grid_data_daily)
        monthly_bias = grid_data_monthly.groupby(['month']).mean()
        for month in monthly_bias.index:
            month_value = monthly_bias.loc[monthly_bias.index==month]
            bias = (month_value.median_era5 / month_value.cmip6_values).to_numpy()
            grid_data_daily.loc[grid_data_daily['month'] == month,'cmip6_values'] = grid_data_daily[grid_data_daily['month'] == month]['cmip6_values'] * bias

        grid_data_daily_bias_corrected = grid_data_daily
        new_data.append(grid_data_daily)

    new_data = pd.concat(new_data)

    for grid in grid_list:
        grid_data_daily_bias_corrected = new_data.loc[new_data.id == grid, :]
        new_data_monthly, new_data_yearly = convert_monthly_yearly_sum(grid_data_daily_bias_corrected)

    return grid_data_daily_bias_corrected, new_data_monthly, new_data_yearly

def rolling():
    data_path = r"./results/access-cm-2.csv"

    data = read_file(data_path)
    grid_list = np.unique(data.id.to_numpy())
    new_data = []
    for grid in grid_list:
        grid_data_daily = data.loc[data.id == grid, :]
        grid_data_daily['date'] = pd.to_datetime(grid_data_daily['date'], format='%Y-%m-%d %H:%M:%S')
        grid_data_daily.set_index('date', inplace=True)
        moving_averages = grid_data_daily.rolling(10,min_periods=1).mean()
        moving_averages['ratio'] = moving_averages.median_era5 / moving_averages.cmip6_values
        grid_data_daily['bias_corrected_cmip6'] = moving_averages.cmip6_values * moving_averages.ratio
        new_data.append(grid_data_daily)

    new_data = pd.concat(new_data)
    new_data.drop(['cmip6_values'], axis=1, inplace=True)
    new_data.rename({'bias_corrected_cmip6': 'cmip6_values'}, axis='columns', inplace=True)

    for grid in grid_list:
        grid_data_daily_bias_corrected = new_data.loc[new_data.id == grid, :]
        new_grid_data_monthly, new_grid_data_yearly = convert_monthly_yearly_sum(grid_data_daily_bias_corrected)

    a = 1
if __name__ == '__main__':
    rolling()
