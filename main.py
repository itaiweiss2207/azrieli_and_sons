# import modules
import pandas as pd
import streamlit as st
from configuration.constants import *
# import files from project
from configuration import read_tables_from_path
from data_checks import numeric_errors
from data_clean import dealing_with_nans
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.display.max_columns = MAX_COLS_TO_DISPLAY
# constants

#TODO "regex, duplicates"


RATES = "rates"
OLD_DRIVERS = "old_drivers"
NEW_DRIVERS = "new_drivers"
BIRTH_DATE = "birth_date"
TOTAL_TIME = "total_time"


def clean_the_tables_data(tables_dict):
    """
    removes nan rows, prints the missing gender and birth-date by id
    :param tables_dict:
    :return:
    """
    for table in tables_dict:
        tables_dict[table] = dealing_with_nans.remove_entire_nan_rows(
            tables_dict[table])
        if table == OLD_DRIVERS or table == NEW_DRIVERS:
            dealing_with_nans.missing_sex_data(tables_dict[table])
    return tables_dict


def clean_drives_data(drives_dict):
    """
    dealing with nans in drives data
    :param drives_dict:
    :return:
    """
    drives_dict = dealing_with_nans.missing_drive_data(drives_dict)
    return drives_dict


def add_time_col(df):
    df[TOTAL_TIME] = df[[START_TIME, END_TIME]].apply(
        lambda x: ((x[END_TIME] - x[START_TIME]).total_seconds()) / SECONDS_IN_HOUR, axis=1)
    return df


def add_kmh_col(df):
    df[SPEED] = df[KM] / df[TOTAL_TIME]
    return df


def clean_add_drives(df):
    df = clean_drives_data(df)
    df = dealing_with_nans.time_for_drives(df)
    df = add_time_col(df)
    df = add_kmh_col(df)
    numeric_errors.check_max_vals(df)

    return df

def main():
    data_dict = read_tables_from_path.read_tables_from_outside()
    drives_data = read_tables_from_path.read_tables_from_dir_outside()
    data_dict = clean_the_tables_data(data_dict)
    drives_data = clean_add_drives(drives_data)
    st.title("first proj")
    st.table(drives_data.head(100))

if __name__ == '__main__':
    main()