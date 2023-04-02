# imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from configuration.constants import *
import streamlit as st


pd.options.display.max_columns = MAX_COLS_TO_DISPLAY

def check_max_vals(df: pd.DataFrame):
    top_km = df[df[KM] > 6000]
    print(top_km[[SPEED, KM]])
    top_kmh = df[(df[SPEED] > 150) & (df[SPEED] < 500)]
    print(top_kmh[[SPEED, KM]])
    st.table(top_kmh[[SPEED, KM]])


