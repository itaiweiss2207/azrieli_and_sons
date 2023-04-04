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
from data_edit import replace_values

pd.options.display.max_columns = MAX_COLS_TO_DISPLAY
from datetime import datetime, timedelta


def timedate_to_night_hours(start_time: datetime, end_time: datetime,
                            extra_time: datetime):
    night_hours = 0
    night_extra_miles_hours = 0
    while start_time < end_time:
        if start_time.minute != 0:
            if (start_time.hour > NIGHT_START_HOUR) or (
                    start_time.hour < NIGHT_END_HOUR):
                if start_time < extra_time:
                    night_hours += (60 - start_time.minute) / 60
                else:
                    night_extra_miles_hours += (60 - start_time.minute) / 60
                start_time += timedelta(minutes=(60 - start_time.minute))
        if end_time.minute != 0:
            if (end_time.hour < NIGHT_END_HOUR) or (
                    end_time.hour > NIGHT_START_HOUR):
                if start_time >= extra_time:
                    night_extra_miles_hours += end_time.minute / 60
                else:
                    night_hours += end_time.minute / 60
                end_time -= timedelta(minutes=end_time.minute)
        if start_time.hour >= NIGHT_START_HOUR or start_time.hour < NIGHT_END_HOUR:
            if start_time >= extra_time:
                night_extra_miles_hours += 1
            else:
                night_hours += 1
        start_time += timedelta(hours=1)
    return night_hours, night_extra_miles_hours


def night_hours_df(df: pd.DataFrame):
    df[[NIGHT_HOURS, EXTRA_MILES_HOURS_NIGHT]] = df.apply(night_hours_row,
                                                          axis=1)
    return df


def night_hours_row(row):
    start = row[START_TIME]
    end = row[END_TIME]
    extra = row[EXTRA_MILES_TIME]
    night_hours, extra_miles_hours = timedate_to_night_hours(start, end, extra)
    return night_hours, extra_miles_hours
