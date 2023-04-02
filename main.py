# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import typing

# constants




def read_tables():
    rate_table: pd.DataFrame = pd.read_csv(
        r"C:\Users\itaiw\OneDrive\Work\DS\azrieli_and_sons\taarif.csv")
    check_table_exist(rate_table)
    new_drivers_table: pd.DataFrame = pd.read_csv(
        r"C:\Users\itaiw\OneDrive\Work\DS\azrieli_and_sons\new_drivers.csv")
    check_table_exist(new_drivers_table)
    exp_drivers_table: pd.DataFrame = pd.read_csv(r"C:\Users\itaiw\OneDrive\Work\DS\azrieli_and_sons\Drivers_with_kviut.csv")
    check_table_exist(exp_drivers_table)

    return rate_table, new_drivers_table, exp_drivers_table


def check_table_exist(data: pd.DataFrame):
    print(data.head())
    print(data.describe())


if __name__ == '__main__':
    rate_table, new_drivers_table, exp_drivers_table = read_tables()


