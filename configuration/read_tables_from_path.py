import pandas as pd
from configuration import paths
import glob
import re
from datetime import datetime
from configuration.constants import *




def read_tables_from_inside():
    """
    uses the paths in configuration file, from inside-scope and loads its data to DataFrame
    :return: dictionary of 3 DataFrames of rates, new_drivers, exp_drivers
    """
    table1: pd.DataFrame = pd.read_csv(paths.RATES_FILE_FROM_INSIDE)
    table2: pd.DataFrame = pd.read_csv(paths.NEW_DRIVERS_FILE_FROM_INSIDE)
    table3: pd.DataFrame = pd.read_csv(paths.EXP_DRIVERS_FILE_FROM_INSIDE)
    dict_of_tables = {RATES: table1, NEW_DRIVERS: table2, OLD_DRIVERS: table3}
    return dict_of_tables

def read_tables_from_outside():
    """
    uses the paths in configuration file, from outside scope, and loads its data to DataFrame
    :return: dictionary of 3 DataFrames of rates, new_drivers, exp_drivers
    """
    table1: pd.DataFrame = pd.read_csv(paths.RATES_FILE_FROM_OUTSIDE)
    table2: pd.DataFrame = pd.read_csv(paths.NEW_DRIVERS_FILE_FROM_OUTSIDE)
    table3: pd.DataFrame = pd.read_csv(paths.EXP_DRIVERS_FILE_FROM_OUTSIDE)
    dict_of_tables = {RATES: table1, NEW_DRIVERS: table2, OLD_DRIVERS: table3}
    return dict_of_tables


def read_tables_from_dir_inside():
    """
    reads all files in a dir, converts it to df and return a dict of them
    :return: dataframe of all the drives in the csv's
    """
    drives_dataframe = pd.DataFrame(columns=COL_NAMES)
    for fname in glob.glob(paths.TRUCK_PATH_INSIDE):
        cur_data = pd.read_csv(fname)
        cur_data.dropna(axis=0, how='all', inplace=True)
        name = re.search(PATTERN_FOR_NAME, fname).group(1)
        cur_data[TRUCK_NAME] = name
        drives_dataframe = drives_dataframe.append(cur_data, ignore_index=True)
    return drives_dataframe

def read_tables_from_dir_outside():
    """
    reads all files in a dir, converts it to df and return a dict of them
    :return: dataframe of all the drives in the csv's
    """
    drives_dataframe = pd.DataFrame(columns=COL_NAMES)
    for fname in glob.glob(paths.TRUCK_PATH_OUTSIDE):
        cur_data = pd.read_csv(fname)
        cur_data.dropna(axis=0, how='all', inplace=True)
        name = re.search(PATTERN_FOR_NAME, fname).group(1)
        cur_data[TRUCK_NAME] = name
        drives_dataframe = drives_dataframe.append(cur_data, ignore_index=True)
    return drives_dataframe
