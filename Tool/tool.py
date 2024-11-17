import pandas as pd
from tabulate import tabulate

def load_csv(file_path):
    return pd.read_csv(file_path)

def sort_data(data, columns, order):
    return data.sort_values(by=columns, ascending=order)

def search_data(data, column, value):
    return data[data[column].astype(str).str.contains(value, case=False)]

def filter_data(data, column, condition):
    return data.query(f"{column} {condition}")

def filter_depression_risk(data):
    """
    Lọc ra các dòng có giá trị 'High' hoặc 'Very High' trong cột 'Depression Risk'.
    """
    return data[data['Depression Risk'].isin(['High', 'Very High'])]

def display_data(data, page_size=10):
    total_rows = len(data)
    current_page = 1
    total_pages = (total_rows + page_size - 1) // page_size

    while True:
        start_row = (current_page - 1) * page_size
        end_row = min(start_row + page_size, total_rows)
        page_data = data.iloc[start_row:end_row]

        print(tabulate(page_data, headers="keys", tablefmt="grid", showindex=False))
        print(f"Trang {current_page}/{total_pages}")

        if total_pages == 1:
            break

        action = input("Nhập 'n' để sang trang sau, 'p' để quay lại trang trước, hoặc 'q' để thoát: ").lower()
        if action == 'n' and current_page < total_pages:
            current_page += 1
        elif action == 'p' and current_page > 1:
            current_page -= 1
        elif action == 'q':
            break
        else:
            print("Lựa chọn không hợp lệ.")
