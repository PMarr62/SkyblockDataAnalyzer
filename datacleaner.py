"""
File Name: datacleaner.py

Helper class to format Pandas DataFrame objects into respective, proper format for
the APIWindow's treeview table.
"""

import pandas as pd

class DataCleaner:
    STRING_COLS = ["Item Name"]
    INT_COLS = ["Buy Price", "Sell Price", "Quantity", "Profit", "Leftover"]
    FLOAT_COLS = ["ROI", "Buy Wait", "Sell Wait", "Total Wait"]

    def format_int_column(self, col: str, df: pd.DataFrame) -> pd.DataFrame:
        if col not in DataCleaner.INT_COLS:
            return df
        df[col] = df[col].astype('int') # convert to int
        df[col] = df[col].astype('object')
        df[col] = df[col].apply(lambda x: f"{x:,}")
        return df
    
    def format_float_column(self, col: str, df: pd.DataFrame) -> pd.DataFrame:
        if col not in DataCleaner.FLOAT_COLS:
            return df
        df[col] = df[col].apply(lambda x: f"{x:,.1f}")
        if col == "ROI":
            df[col] = df[col].astype(str) + "%"
        return df


    def run_clean(self, df: pd.DataFrame) -> pd.DataFrame:
        #Remove NAN rows
        df.dropna(subset=DataCleaner.STRING_COLS + DataCleaner.INT_COLS, inplace=True)

        #Remove <= 0 Rows
        df.drop(df[df['Profit'] <= 0].index, inplace=True)

        #Converting capital underscore items to human-readable
        df['Item Name'] = df['Item Name'].str.replace("_", " ").str.title()
        
        for int_column in DataCleaner.INT_COLS:
            df = self.format_int_column(int_column, df)
        for float_column in DataCleaner.FLOAT_COLS:
            df = self.format_float_column(float_column, df)
        return df
