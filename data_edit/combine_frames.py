import pandas as pd


def comb_frames(df1:pd.DataFrame, df2: pd.DataFrame):
    df_concat = pd.concat([df1, df2], ignore_index=True)
    return df_concat