import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistical_methods import calculate_md, calculate_kge, calculate_nrmse


def read_file(path):
    df = pd.read_csv(path)
    return df

def convert_monthly_yearly_sum(df):
    df['year'] = df.index.year
    df['month'] = df.index.month
    monthly_data = df.groupby(['year','month']).sum()
    yearly_data = df.groupby('year').sum()
    return monthly_data, yearly_data

def convert_monthly_yearly_mean(df):
    df['year'] = df.index.year
    df['month'] = df.index.month
    monthly_data = df.groupby(['year','month']).mean()
    yearly_data = df.groupby('year').mean()
    return monthly_data, yearly_data


if __name__ == '__main__':
    input = r"./results/access-cm-2.csv"
    data = read_file(input)

    best_grid = 61

    grid_data = data.loc[data.id==best_grid, :]
    del data

    grid_data['date'] = pd.to_datetime(grid_data['date'], format='%Y-%m-%d %H:%M:%S')
    grid_data.set_index('date', inplace=True)

    fig = plt.figure()
    fig.set_figheight(15)
    fig.set_figwidth(15)

    x = grid_data.index
    y1 = grid_data.cmip6_values
    y2 = grid_data.max_era5

    plt.scatter(x=y2, y=y1)
    plt.grid()
    #plt.show()

    monthly, yearly = convert_monthly_yearly(grid_data)

    y1 = monthly.cmip6_values
    y2 = monthly.max_era5
    plt.scatter(x=y2, y=y1)
    plt.grid()
    plt.show()


    a = 1

