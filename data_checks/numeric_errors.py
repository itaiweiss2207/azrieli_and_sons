# imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from configuration.constants import *
import streamlit as st


pd.options.display.max_columns = MAX_COLS_TO_DISPLAY



def check_max_vals(df: pd.DataFrame):
    top_km = df[df[KM] > TOO_LONG_DISTANCE]
    print(top_km[[SPEED, KM]])
    top_kmh = df[(df[SPEED] > TOO_HIGH_SPEED) & (df[SPEED] < UNREAL_SPEED)]
    print(top_kmh[[SPEED, KM]])
    st.table(top_kmh[[SPEED, KM]])


def taarif_show_wierd_stuff(df: pd.DataFrame):
    """

    :param df:
    :return:
    """
    print(df.describe())
    for col in df.select_dtypes(include=['number']):
        sns.boxplot(y=col, data=df)

        plt.show()


def taarif_find_wierd_stats(df: pd.DataFrame):
    for col in df.select_dtypes(include=['number']):
        if col != BASIC_TAARIF:
            str_for_col = "MAX_FOR_" + col.upper()
            non_logic = df[df[col] > globals()[str_for_col]]
            print(f"the non logic values for {col} are:\n {non_logic}")
