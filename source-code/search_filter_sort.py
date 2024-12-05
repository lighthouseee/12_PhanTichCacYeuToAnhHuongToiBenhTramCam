import pandas as pd
import numpy as np

# Đường dẫn file CSV
CSV_FILE = "dataset\\cleaned_and_predicted_data.csv"

# Đọc dữ liệu từ file CSV
def read_csv_data():
    """
    Đọc dữ liệu từ file CSV
    :return: DataFrame chứa dữ liệu
    """
    try:
        data = pd.read_csv(CSV_FILE)
        print(f"Đã đọc thành công dữ liệu từ file '{CSV_FILE}'.")
        return data
    except FileNotFoundError:
        print(f"Lỗi: File '{CSV_FILE}' không tồn tại.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return pd.DataFrame()
               
def sort_data(data, column, ascending=True):
    """Sắp xếp dữ liệu theo cột."""
    if column not in data.columns:
        raise ValueError(f"Cột '{column}' không tồn tại.")
    return data.sort_values(by=column, ascending=ascending, ignore_index=True)

def filter_data(data, column, value):
    if column not in data.columns:
        raise ValueError(f"Cột '{column}' không tồn tại.")
    return data[data[column].astype(str).str.contains(value, case=False, na=False)].reset_index(drop=True)

# Lọc dữ liệu nguy cơ trầm cảm cao
def filter_depression_risk(data):
    """
    Lọc các dòng có giá trị 'High' hoặc 'Very High' trong cột 'Depression Risk'.
    """
    column = 'Depression Risk'
    if column not in data.columns:
        print(f"Lỗi: Cột '{column}' không tồn tại trong dữ liệu.")
        return pd.DataFrame()
    filtered_data = data[data[column].isin(['High', 'Very High'])]
    print(f"Đã lọc thành công {len(filtered_data)} dòng có nguy cơ trầm cảm cao.")
    filtered_data.to_csv("filtered_depression_data.csv", index=False)
    print("Đã lưu trữ dữ liệu vào file 'filtered_depression_data.csv'.")
    return filtered_data
