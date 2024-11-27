import pandas as pd
import numpy as np

def sort_data(data, column, ascending=True):
    """Sắp xếp dữ liệu theo cột."""
    if column not in data.columns:
        raise ValueError(f"Cột '{column}' không tồn tại.")
    return data.sort_values(by=column, ascending=ascending, ignore_index=True)

def filter_data(data, column, value):
    if column not in data.columns:
        raise ValueError(f"Cột '{column}' không tồn tại.")
    return data[data[column].astype(str).str.contains(value, case=False, na=False)].reset_index(drop=True)

