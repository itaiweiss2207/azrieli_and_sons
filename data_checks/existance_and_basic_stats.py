#imports
import pandas as pd
from configuration import read_tables_from_path
from configuration.constants import *


def check_table_exist(data: pd.DataFrame):
    # print(data.head())
    # print(data.describe())
    pass

def print_head_and_description():
    dict_of_tables = read_tables_from_path.read_tables_from_inside()
    for table in dict_of_tables:
        check_table_exist(table)


#TODO delete


