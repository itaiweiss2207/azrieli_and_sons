# imports
import pandas as pd
from configuration.constants import *



def remove_entire_nan_rows(df: pd.DataFrame):
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


def time_for_drives(df: pd.DataFrame):
    """
    replace nan in start_time and end_time with the other, and convert them to datetime
    :param df:
    :return: the updated df
    """
    df[START_TIME] = df.apply(lambda x: x[END_TIME] if (
                (pd.isna(x[START_TIME])) & (not pd.isna(x[END_TIME]))) else x[
        START_TIME], axis=1)
    df[END_TIME] = df.apply(lambda x: x[START_TIME] if (
                (pd.isna(x[END_TIME])) & (not pd.isna(x[START_TIME]))) else x[
        END_TIME], axis=1)
    df[START_TIME] = pd.to_datetime(df[START_TIME], infer_datetime_format=True)
    df[END_TIME] = pd.to_datetime(df[END_TIME], infer_datetime_format=True)
    return df


