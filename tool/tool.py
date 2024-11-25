import pandas as pd

# Đường dẫn file CSV
CSV_FILE = "cleaned_and_predicted_data.csv"

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

# Hiển thị danh sách các cột dưới dạng số thứ tự
def display_columns(data):
    column_mapping = {str(i + 1): col for i, col in enumerate(data.columns)}
    print("Danh sách các cột hiện có trong dữ liệu:")
    for idx, col in column_mapping.items():
        print(f"{idx}. {col}")
    return column_mapping

# Sắp xếp dữ liệu
def sort_data(data):
    """
    Sắp xếp dữ liệu theo các cột chỉ định và chỉ hiển thị cột Name cùng cột sắp xếp.
    """
    column_mapping = display_columns(data)
    while True:
        col_number = input("Nhập số thứ tự của cột muốn sắp xếp: ").strip()
        if col_number in column_mapping:
            column = column_mapping[col_number]
            break
        else:
            print("Lỗi: Số không hợp lệ. Vui lòng thử lại.")
    
    order = input(f"Thứ tự sắp xếp cho cột '{column}' (tăng? y/n): ").strip().lower()
    ascending = order == "y"
    
    print(f"Sắp xếp theo cột: {column}, Thứ tự: {'tăng' if ascending else 'giảm'}.")
    sorted_data = data.sort_values(by=column, ascending=ascending)
    return sorted_data[["Name", column]]

# Tìm kiếm dữ liệu
def search_data(data):
    """
    Tìm kiếm các dòng có giá trị chứa từ khóa trong cột chỉ định 
    và chỉ hiển thị cột Name cùng cột tìm kiếm. Hiển thị các từ khóa có thể tìm kiếm dưới dạng đánh số.
    """
    column_mapping = display_columns(data)
    while True:
        col_number = input("Nhập số thứ tự của cột muốn tìm kiếm: ").strip()
        if col_number in column_mapping:
            column = column_mapping[col_number]
            break
        else:
            print("Lỗi: Số không hợp lệ. Vui lòng thử lại.")
    
    # Hiển thị các từ khóa có thể tìm kiếm và đánh số
    unique_values = sorted(data[column].dropna().unique())
    print(f"Các từ khóa có thể tìm kiếm trong cột '{column}':")
    value_mapping = {str(i + 1): value for i, value in enumerate(unique_values)}
    for idx, value in value_mapping.items():
        print(f"{idx}. {value}")
    
    # Nhập số tương ứng thay vì nhập toàn bộ từ khóa
    while True:
        selected_number = input("Nhập số tương ứng với từ khóa tìm kiếm: ").strip()
        if selected_number in value_mapping:
            keyword = value_mapping[selected_number]
            break
        else:
            print("Lỗi: Số không hợp lệ. Vui lòng thử lại.")
    
    print(f"Tìm kiếm các dòng chứa từ khóa '{keyword}' trong cột '{column}'.")
    
    # Tìm kiếm dữ liệu
    filtered_data = data[data[column].astype(str).str.contains(keyword, case=False, na=False)]
    if filtered_data.empty:
        print("Không tìm thấy dòng nào chứa từ khóa.")
        return pd.DataFrame(columns=["Name", column])  # Trả về DataFrame trống với các cột tương ứng
    else:
        print(f"Tìm thấy {len(filtered_data)} dòng chứa từ khóa.")
        return filtered_data[["Name", column]]

# Lọc dữ liệu
def filter_data(data):
    """
    Lọc dữ liệu theo điều kiện và chỉ hiển thị cột Name cùng cột lọc.
    """
    column_mapping = display_columns(data)
    while True:
        col_number = input("Nhập số thứ tự của cột muốn lọc: ").strip()
        if col_number in column_mapping:
            column = column_mapping[col_number]
            break
        else:
            print("Lỗi: Số không hợp lệ. Vui lòng thử lại.")
    
    unique_values = data[column].dropna().unique()
    unique_values_sorted = sorted(unique_values)
    print(f"Giá trị khả dụng trong cột '{column}':")
    for i, value in enumerate(unique_values_sorted, start=1):
        print(f"{i}. {value}")
    
    while True:
        condition = input(f"Nhập điều kiện lọc (ví dụ: '1' hoặc '> 25'): ").strip()
        try:
            if condition.isdigit() and int(condition) <= len(unique_values_sorted):
                condition = f'== "{unique_values_sorted[int(condition)-1]}"'
            break
        except Exception:
            print("Điều kiện không hợp lệ. Vui lòng thử lại.")
    
    try:
        filtered_data = data.query(f"`{column}` {condition}")
        if filtered_data.empty:
            print("Không có dữ liệu nào thỏa mãn điều kiện.")
        else:
            print("Đã lọc thành công.")
        return filtered_data[["Name", column]]
    except Exception as e:
        print(f"Lỗi khi áp dụng bộ lọc: {e}")
        return pd.DataFrame()

# Lọc theo nguy cơ trầm cảm cao
def filter_depression_risk(data):
    """
    Lọc ra các dòng có giá trị 'High' hoặc 'Very High' trong cột 'Depression Risk' và chỉ hiển thị cột Name cùng cột nguy cơ.
    """
    column = 'Depression Risk'  
    if column not in data.columns:
        print(f"Lỗi: Cột '{column}' không tồn tại trong dữ liệu.")
        return pd.DataFrame()
    
    print(f"Lọc các dòng có rủi ro trầm cảm 'High' hoặc 'Very High' trong cột '{column}'.")
    filtered_data = data[data[column].isin(['High', 'Very High'])]
    if filtered_data.empty:
        print("Không có dữ liệu nào thỏa mãn điều kiện.")
    else:
        print("Đã lọc thành công.")
    filtered_data = filtered_data[["Name", column]]
    filtered_data.to_csv("filtered_depression_data.csv", index=False)
    print("Đã lưu trữ dữ liệu vào file filtered_depression_data.csv")
    return filtered_data

