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

def final_df(drives: pd.DataFrame, drivers: pd.DataFrame):
    columns_names = [FINAL_DRIVER_ID, FINAL_MONTH, FINAL_TOTAL_INCOME, FINAL_TOTAL_KM, FINAL_GENDER, FINAL_AGE, FINAL_VETEK]
    final_data = pd.DataFrame(columns=columns_names)
    final_data[FINAL_DRIVER_ID] = drivers[ID]
    final_data.set_index(FINAL_DRIVER_ID)
    final_data.loc[final_data[FINAL_DRIVER_ID].isin(drivers[ID]), FINAL_AGE] = drivers.set_index(ID)[AGE]
    final_data.loc[final_data[FINAL_DRIVER_ID].isin(drivers[ID]), FINAL_VETEK] = \
    drivers.set_index(ID)[VETEK]
    final_data.loc[final_data[FINAL_DRIVER_ID].isin(drivers[ID]), FINAL_GENDER] = \
    drivers.set_index(ID)[GENDER]
    final_data.loc[FINAL_MONTH] = MONTH_FOR_FINAL_DATA
    drives_by_id = drives.groupby(by=DRIVER_ID)
    drivers_salary = drives_by_id[PAYMENT].sum()
    drivers_total_km = drives_by_id[KM].sum()
    final_data.loc[final_data[FINAL_DRIVER_ID].isin(drivers_salary), FINAL_TOTAL_INCOME] = drivers_salary[FINAL_DRIVER_ID]
    final_data.loc[
        final_data[FINAL_DRIVER_ID].isin(drivers_total_km), FINAL_TOTAL_KM] = \
    drivers_total_km[FINAL_DRIVER_ID]
    print(final_data.head(20))

    return final_data