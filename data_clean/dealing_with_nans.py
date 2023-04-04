# imports
import datetime
import numpy as np
import pandas as pd
from configuration.constants import *

#TODO return hints
def remove_entire_nan_rows(df: pd.DataFrame)->pd.DataFrame:
    """
    removes nan rows
    :param df:
    :return:
    """
    df.dropna(axis=0, how='all', inplace=True)
    return df


def missing_sex_data(df: pd.DataFrame):
    """
    prints the id's that we dont have their gender
    :param df:
    :return:
    """
    missing = df[df[GENDER].isna()]
    missing_id = missing[ID].values.tolist()
    print(f"missing gender for id: \n {missing_id}")


def missing_date_data(df: pd.DataFrame):
    """

    :param df:
    :return:
    """
    missing = df[df[BIRTH_DATE].isna()]
    print(missing)
    missing_id = missing[ID].values.tolist()
    print(f"missing birth date for id: \n {missing_id}")


def missing_drive_data(df: pd.DataFrame):
    """
    finding where is the nan values
    :param df:
    :return:
    """
    for col in df.columns:
        missing = df[df[col].isna()]
        if not missing.empty:
            print(f"missing stuff for: {col} \n {missing}")
    no_known_time = df.loc[(df[START_TIME].isna()) & (df[END_TIME].isna())]
    print(f"need time_data for:\n {no_known_time}")
    return df


def nans_in_time(df: pd.DataFrame):
    """

    :param df:
    :return:
    """
    print(df.head(5))
    df[START_TIME] = df[START_TIME].apply(
        lambda x: pd.to_datetime(x, infer_datetime_format=True) if pd.notna(x) else 0)
    df[END_TIME] = df[END_TIME].apply(
        lambda x: pd.to_datetime(x, infer_datetime_format=True) if pd.notna(x) else 0)

    df[TOTAL_TIME] = df[[START_TIME, END_TIME]].apply(
        lambda x: ((x[END_TIME] - x[START_TIME]).total_seconds()) / SECONDS_IN_HOUR if x[START_TIME]!= 0 and x[END_TIME]!=0 else 0, axis=1)
    return df
