# import modules
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, time
from configuration.constants import *
# import files from project
from configuration import read_tables_from_path
from data_checks import numeric_errors
from data_clean import dealing_with_nans
import seaborn as sns
import matplotlib.pyplot as plt
from data_edit import replace_values
from data_edit import advanced_calcs
pd.options.display.max_columns = MAX_COLS_TO_DISPLAY


def add_hour_of_start_end_drive(df: pd.DataFrame):
    df[START_HOUR] = df[START_TIME].hour
    df[END_HOUR] = df[END_TIME].hour


def add_age_for_driver(df: pd.DataFrame):
    current_date = datetime.now()
    age = current_date - df[BIRTH_DATE]
    age_years = age.dt.days / 365.25  # divide by average number of days in a year
    # Check if age is greater than 100 and set it to 'unknown'
    age_years[age_years > 100] = 'unknown'
    # Round the age to one decimal point
    age_rounded = age_years.apply(
        lambda x: round(x, 1) if isinstance(x, float) else x)

    # Add the age to the DataFrame
    df[AGE] = age_rounded
    return df

# TODO make everything readable
def forward_to_weekend(dt):
    if dt.weekday() not in [4,5] or (dt.weekday() == 4 and dt.hour < WEEKEND_START_HOUR_IN_FRIDAY):
        days_to_friday = (4 - dt.weekday()) % 7
        next_friday = dt + timedelta(days=days_to_friday)

        # Set the time to 4 PM
        next_friday_4pm = next_friday.replace(hour=16, minute=0, second=0,
                                              microsecond=0)
        return next_friday_4pm
    else:
        return dt


def backward_to_weekend(dt):
    if dt.weekday() not in [4,5] or (dt.weekday() == 5 and dt.hour > WEEKEND_END_HOUR_IN_SATURDAY):
        next_sunday = dt + timedelta(days=(6 - dt.weekday()))

        # Set the time to 20:00
        last_before_sunday_2000 = datetime.combine(next_sunday,
                                                   datetime.min.time()) + timedelta(
            hours=20)

        # If the last_before_sunday_2000 is in the future, subtract one week
        if last_before_sunday_2000 > dt:
            last_before_sunday_2000 -= timedelta(weeks=1)

        return last_before_sunday_2000
    else:
        return dt


def weekend_hours_from_time(start:datetime, end:datetime, extra: datetime):
    weekend_day_no_extra_hours = 0
    weekend_day_extra_hours = 0
    weekend_night_no_extra_hours = 0
    weekend_night_yes_extra_hours = 0
    updated_start = forward_to_weekend(start)
    updated_end = backward_to_weekend(end)
    while updated_start < updated_end:
        if updated_start.minute != 0:
            if updated_start.weekday() == 4 and updated_start.hour >= WEEKEND_START_HOUR_IN_FRIDAY:
                if updated_start.hour >= NIGHT_START_HOUR:
                    if updated_start >= extra:
                        weekend_night_yes_extra_hours += (60 - updated_start.minute) / 60
                    else:
                        weekend_night_no_extra_hours  += (60 - updated_start.minute) / 60
                else:
                    if updated_start >= extra:
                        weekend_day_extra_hours  += (60 - updated_start.minute) / 60
                    else:
                        weekend_day_no_extra_hours  += (60 - updated_start.minute) / 60
            elif updated_start.weekday() == 5 and updated_start.hour < WEEKEND_END_HOUR_IN_SATURDAY:
                if updated_start.hour < NIGHT_END_HOUR:
                    if updated_start > extra:
                        weekend_night_yes_extra_hours += (60 - updated_start.minute) / 60
                    else:
                        weekend_night_no_extra_hours += (60 - updated_start.minute) / 60
                else:
                    if updated_start > extra:
                        weekend_day_extra_hours += (60 - updated_start.minute) / 60
                    else:
                        weekend_day_no_extra_hours += (60 - updated_start.minute) / 60
            updated_start += timedelta(minutes=60 - updated_start.minute)
        if updated_end.minute != 0 and updated_end.hour < WEEKEND_END_HOUR_IN_SATURDAY:
            if updated_end.hour < NIGHT_END_HOUR:
                if updated_end > extra:
                    weekend_night_yes_extra_hours += updated_end.minute / 60
                else:
                    weekend_night_no_extra_hours += updated_end.minute / 60
            else:
                if updated_start > extra:
                    weekend_day_extra_hours += updated_end.minute / 60
                else:
                    weekend_day_no_extra_hours += updated_end.minute / 60
            updated_end -= timedelta(minutes=updated_end.minute)
        else:
            if updated_start.weekday() == 4 and (updated_start.hour >= WEEKEND_START_HOUR_IN_FRIDAY):
                if updated_start.hour >= NIGHT_START_HOUR:
                    if updated_start > extra:
                        weekend_night_yes_extra_hours += 1
                    else:
                        weekend_night_no_extra_hours += 1
                else:
                    if updated_start > extra:
                        weekend_day_extra_hours += 1
                    else:
                        weekend_day_no_extra_hours += 1
            elif updated_start.weekday() == 5 and (updated_start.hour < WEEKEND_END_HOUR_IN_SATURDAY):
                if updated_start.hour < NIGHT_END_HOUR:
                    if updated_start > extra:
                        weekend_night_yes_extra_hours += 1
                    else:
                        weekend_night_no_extra_hours += 1
                else:
                    if updated_start > extra:
                        weekend_day_extra_hours += 1
                    else:
                        weekend_day_no_extra_hours += 1
            updated_start += timedelta(hours=1)
    return weekend_night_yes_extra_hours, weekend_night_no_extra_hours, weekend_day_extra_hours, weekend_day_no_extra_hours


def weekend_from_row(row: pd.Series):
    start = row[START_TIME]
    end = row[END_TIME]
    extra = row[EXTRA_MILES_TIME]
    weekend_night_extra, weekend_night_no_extra, weekend_day_extra, weekend_day_no_extra = weekend_hours_from_time(start, end, extra)
    return weekend_night_extra, weekend_night_no_extra, weekend_day_extra, weekend_day_no_extra


def add_weekend_hours(df: pd.DataFrame):
    df[[WEEKEND_HOURS_YES_EXTRA_YES_NIGHT, WEEKEND_HOURS_NO_EXTRA_YES_NIGHT, WEEKEND_HOURS_YES_EXTRA_NO_NIGHT, WEEKEND_HOURS_NO_EXTRA_NO_NIGHT]] = df.apply(weekend_from_row, axis=1)
    df[NIGHT_HOURS] = df[NIGHT_HOURS] - (df[WEEKEND_HOURS_NO_EXTRA_YES_NIGHT] + df[WEEKEND_HOURS_YES_EXTRA_YES_NIGHT] + df[EXTRA_MILES_HOURS_NIGHT])
    return df


def add_extra_miles_time(df: pd.DataFrame):
    df[EXTRA_MILES_TIME] = df[START_TIME] + timedelta(hours=(200/df[SPEED]))
    return df


def row_to_payment(row: pd.Series, fares: pd.DataFrame):
    mean_speed = row[SPEED]
    relevant_customer = fares[fares[CUSTOMER] == row[CUSTOMER]]
    basic = relevant_customer.iloc[0][BASIC_TAARIF]
    night = basic + relevant_customer.iloc[0][NIGHT_BONUS]
    weekend = relevant_customer.iloc[0][WEEKEND_BONUS]
    extra_mile = relevant_customer.iloc[0][EXTRA_MILAGE]
    weekend_extra_night_km = row[WEEKEND_HOURS_YES_EXTRA_YES_NIGHT] * mean_speed
    weekend_extra_day_km = row[WEEKEND_HOURS_YES_EXTRA_NO_NIGHT] * mean_speed
    weekend_no_extra_night_km = row[WEEKEND_HOURS_NO_EXTRA_YES_NIGHT] * mean_speed
    weekend_no_extra_no_night_km = row[WEEKEND_HOURS_NO_EXTRA_NO_NIGHT] * mean_speed
    extra_no_night = row[EXTRA_MILAGE] - (row[EXTRA_MILES_HOURS_NIGHT] + )
    payment = row[KM] * basic + row[NIGHT_HOURS] * night + row[WEEKEND_HOURS]*weekend + row[EXTRA_MILAGE]*extra_mile
    return payment


def add_drive_payment(df: pd.DataFrame, fares: pd.DataFrame):
    df[PAYMENT] = df.apply(lambda x: row_to_payment(x, fares), axis=1)
    return df


def add_extra_mil_col(df: pd.DataFrame):
    df[EXTRA_MILAGE] = df[KM] - 200
    return df
