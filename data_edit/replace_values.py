# import modules
import datetime

import pandas as pd
import streamlit as st
from configuration.constants import *
# import files from project
from configuration import read_tables_from_path
from data_checks import numeric_errors
from data_clean import dealing_with_nans
from data_edit.new_stats_from_costumer import *
import seaborn as sns
import matplotlib.pyplot as plt
pd.options.display.max_columns = MAX_COLS_TO_DISPLAY


def replace_non_real_drive_time(df: pd.DataFrame):
    # given with over 8000 km
    df.at[2201, TOTAL_TIME] = 41.31667
    df.at[2201, KM] = 41.31667 * df.at[2201, SPEED]
    df.at[2201, START_TIME] = df.at[2201, END_TIME] - datetime.timedelta(
                hours=df.at[2201, KM] / df.at[2201, SPEED])
    # given with no start or end time
    df.at[12401, END_TIME] = df.at[12400, END_TIME]
    df.at[12401, START_TIME] = df.at[12401, END_TIME] - datetime.timedelta(
        hours=df.at[12401, KM] / df.at[12401, SPEED])
    df.at[12401, TOTAL_TIME] = df.at[12400, END_TIME] - df.at[12400, START_TIME]
    return df



def repalce_rates(df: pd.DataFrame):
    """

    :param df:
    :return:
    """
    df.at[1, EXTRA_MILAGE] = NEW_EXTRA_JERUS
    df.at[9, NIGHT_BONUS] = NEW_EXTRA_IAF
    df.at[11, WEEKEND_BONUS] = NEW_EXTRA_WEEKEND
    df.at[11, EXTRA_MILAGE] = 0
    df.at[12, BASIC_TAARIF] = 5
    df.at[12, EXTRA_MILAGE] = 0
    df.at[12, WEEKEND_BONUS] = 0
    df.at[12, NIGHT_BONUS] = 0
    df.at[9, WEEKEND_BONUS] = 50
    return df


def find_mean_real_speed(df: pd.DataFrame):
    filtered = df[df[SPEED] < TOO_HIGH_SPEED]
    return filtered[SPEED].mean()


def replace_speeds(df: pd.DataFrame):
    speed_to_place = find_mean_real_speed(df)
    mask = df[SPEED] >= 150
    df.loc[mask, SPEED] = speed_to_place
    return df


def replace_time(df: pd.DataFrame):
    """
    replace nan in start_time and end_time with the other, and convert them to datetime
    :param df:
    :return: the updated df
    """
    df = df.apply(lambda row: update_row(row), axis=1)
    df[TOTAL_TIME] = df[[START_TIME, END_TIME]].apply(
        lambda x: ((x[END_TIME] - x[
            START_TIME]).total_seconds()) / SECONDS_IN_HOUR if x[
                                                                   START_TIME] != 0 and
                                                               x[
                                                                   END_TIME] != 0 else 0,
        axis=1)
    return df


def update_row(row):
    if row[TOTAL_TIME] == 0:
        if row[START_TIME] == 0 and row[END_TIME] == 0:
            pass
        else:
            if row[START_TIME] == 0:
                row[START_TIME] = row[END_TIME] - datetime.timedelta(
                hours=row[KM] / row[SPEED])
            elif row[END_TIME] == 0:
                row[END_TIME] = row[START_TIME] + datetime.timedelta(
                    hours=row[KM] / row[SPEED])
    return row


def time_format(df: pd.DataFrame):
    df[BIRTH_DATE] = df[BIRTH_DATE].apply(lambda x: pd.to_datetime(x, infer_datetime_format=True))
    return df


def vetek_from_days_to_years(df: pd.DataFrame):
    df[VETEK] = df[VETEK] / 365
    return df