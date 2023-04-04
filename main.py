# import modules
from datetime import datetime

import pandas as pd
import streamlit as st
from configuration.constants import *
# import files from project
from configuration import read_tables_from_path
from data_checks import numeric_errors
from data_clean import dealing_with_nans
import seaborn as sns
import matplotlib.pyplot as plt
from data_edit import replace_values
from data_edit import advanced_calcs
from data_edit import columns_add
from data_edit import combine_frames
from final_dataframe import final
pd.options.display.max_columns = MAX_COLS_TO_DISPLAY
# constants


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
            tables_dict[table] = replace_values.time_format(tables_dict[table])
            tables_dict[table] = columns_add.add_age_for_driver(tables_dict[table])
        else:
            tables_dict[table] = replace_values.repalce_rates(tables_dict[table])

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
    df = dealing_with_nans.nans_in_time(df)
    df = add_kmh_col(df)
    numeric_errors.check_max_vals(df)
    df = replace_values.replace_speeds(df)
    df = replace_values.replace_time(df)
    df = replace_values.replace_non_real_drive_time(df)
    return df


def stl(df):
    st.title("first proj")
    st.table(df.head(100))


def main():
    data_dict = read_tables_from_path.read_tables_from_outside()
    drives_data: pd.DataFrame = read_tables_from_path.read_tables_from_dir_outside()
    data_dict = clean_the_tables_data(data_dict)
    drives_data = clean_add_drives(drives_data)
    data_dict[RATES] = replace_values.repalce_rates(data_dict[RATES])
    rates_table = data_dict[RATES]
    old_drivers = data_dict[OLD_DRIVERS]
    new_drivers = data_dict[NEW_DRIVERS]
    new_drivers = replace_values.vetek_from_days_to_years(new_drivers)
    drivers_table = combine_frames.comb_frames(old_drivers, new_drivers)
    drives_data = columns_add.add_extra_miles_time(drives_data)
    drives_data = advanced_calcs.night_hours_df(drives_data)
    drives_data = columns_add.add_weekend_hours(drives_data)
    drives_data = columns_add.add_extra_mil_col(drives_data)
    drives_data = columns_add.add_drive_payment(drives_data, rates_table)
    final_table = final.final_df(drives_data, drivers_table)



if __name__ == '__main__':
    main()