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

# Sắp xếp dữ liệu
def sort_data(data, columns=None, ascending=None):
    """
    Sắp xếp dữ liệu theo các cột chỉ định
    :param data: DataFrame
    :param columns: Danh sách các cột cần sắp xếp
    :param ascending: True/False hoặc danh sách True/False xác định thứ tự sắp xếp
    """
    # Chuyển tất cả các tên cột trong dữ liệu về chữ thường
    data.columns = [col.lower() for col in data.columns]
    
    if columns is None:
        print("Danh sách các cột hiện có trong dữ liệu:")
        print(list(data.columns))
        columns = input("Nhập tên các cột muốn sắp xếp (phân cách bằng dấu phẩy nếu nhiều cột): ").strip().split(',')
    
    columns = [col.strip().lower() for col in columns]
    
    # Kiểm tra các cột nhập vào có tồn tại trong dữ liệu hay không
    for col in columns:
        if col not in data.columns:
            print(f"Lỗi: Cột '{col}' không tồn tại trong dữ liệu.")
            return data  # Trả về dữ liệu gốc nếu cột không tồn tại
    
    if ascending is None:
        print("Nhập thứ tự sắp xếp cho từng cột:")
        ascending = []
        for col in columns:
            order = input(f"Thứ tự sắp xếp cho cột '{col}' (tăng? y/n): ").strip().lower()
            ascending.append(order == "y")  # "y" tương ứng True (tăng), "n" tương ứng False (giảm)
    
    if len(ascending) != len(columns):
        print("Lỗi: Số thứ tự tăng/giảm phải khớp với số cột.")
        return data
    
    print(f"Sắp xếp theo cột: {columns}, Thứ tự: {' / '.join(['tăng' if asc else 'giảm' for asc in ascending])}.")
    return data.sort_values(by=columns, ascending=ascending)

# Tìm kiếm dữ liệu
def search_data(data, column=None, keyword=None):
    """
    Tìm kiếm các dòng có giá trị chứa từ khóa trong cột chỉ định
    :param data: DataFrame
    :param column: Cột cần tìm kiếm
    :param keyword: Từ khóa tìm kiếm
    """
    # Chuyển tên cột trong dữ liệu về chữ thường
    data.columns = [col.lower() for col in data.columns]
    
    if column is None or keyword is None:
        print("Danh sách các cột hiện có trong dữ liệu:")
        print(list(data.columns))
        column = input("Nhập tên cột muốn tìm kiếm: ").strip().lower()  
        keyword = input("Nhập từ khóa tìm kiếm: ").strip()
    
    if column not in data.columns:
        print(f"Lỗi: Cột '{column}' không tồn tại trong dữ liệu.")
        return pd.DataFrame()
    
    print(f"Tìm kiếm các dòng chứa từ khóa '{keyword}' trong cột '{column}'.")
    return data[data[column].astype(str).str.contains(keyword, case=False, na=False)]

import pandas as pd

import pandas as pd

def filter_data(data, column=None, condition=None):
    """
    Lọc dữ liệu theo điều kiện
    :param data: DataFrame
    :param column: Cột cần áp dụng bộ lọc
    :param condition: Điều kiện lọc (chuỗi hoặc giá trị thực)
    :return: DataFrame đã được lọc
    """

    # Chuyển tên cột trong dữ liệu về chữ thường    
    data.columns = [col.lower() for col in data.columns]

    if column is None or condition is None:
        print("Danh sách các cột hiện có trong dữ liệu với kiểu dữ liệu:")
        
        # In ra tên cột và kiểu dữ liệu dtype
        for col in data.columns:
            print(f"{col}: {data[col].dtype}")

        # Lấy tên cột từ người dùng
        while True:
            column = input("Nhập tên cột muốn lọc: ").strip().lower()
            if column in data.columns:
                break
            else:
                print(f"Lỗi: Cột '{column}' không tồn tại trong dữ liệu. Vui lòng thử lại.")

        # Kiểm tra và ép kiểu cột (nếu có thể)
        if pd.api.types.is_numeric_dtype(data[column]):
            # Nếu là kiểu chuỗi có thể chuyển thành số, ép kiểu
            data[column] = pd.to_numeric(data[column], errors='coerce')
            is_numeric = True
            print(f"Cột '{column}' được nhận diện là SỐ. Bạn có thể sử dụng các toán tử số: '>', '<', '>=', '<=', '=='.")
        else:
            is_numeric = False
            print(f"Cột '{column}' được nhận diện là CHUỖI. Bạn có thể sử dụng các toán tử chuỗi: '==', '!='.")

        # Kiểm tra lại kiểu dữ liệu sau khi ép kiểu
        if is_numeric and not pd.api.types.is_numeric_dtype(data[column]):
            print(f"Lỗi: Cột '{column}' không thể ép kiểu thành số.")
            return pd.DataFrame()

        # Hiển thị giá trị duy nhất của cột
        unique_values = data[column].dropna().unique()
        
        # Sắp xếp các giá trị với việc giữ kiểu dữ liệu gốc
        unique_values_sorted = sorted(unique_values)

        print(f"Giá trị khả dụng trong cột '{column}':")
        value_mapping = {str(idx + 1): value for idx, value in enumerate(unique_values_sorted)}
        for idx, value in value_mapping.items():
            print(f"{idx}. {value}")

        # Nhập điều kiện lọc
        while True:
            user_input = input("Nhập điều kiện lọc (ví dụ: '1' hoặc '> 25'): ").strip()
            if not is_numeric and user_input in value_mapping:
                condition = f'== "{value_mapping[user_input]}"'
                break
            elif is_numeric:
                condition = user_input
                break
            else:
                print("Điều kiện không hợp lệ. Vui lòng thử lại.")

    # Áp dụng lọc dữ liệu
    print(f"Lọc dữ liệu với điều kiện: `{column}` {condition}.")
    try:
        # Áp dụng query
        filtered_data = data.query(f"`{column}` {condition}")
        if filtered_data.empty:
            print("Không có dữ liệu nào thỏa mãn điều kiện.")
        else:
            print("Đã lọc thành công.")
        return filtered_data
    except Exception as e:
        print(f"Lỗi khi áp dụng bộ lọc: {e}")
        return pd.DataFrame()




# Lọc theo nguy cơ trầm cảm cao
def filter_depression_risk(data):
    """
    Lọc ra các dòng có giá trị 'High' hoặc 'Very High' trong cột 'Depression Risk'.
    """
    column = 'Depression Risk'  
    if column not in data.columns:
        print(f"Lỗi: Cột '{column}' không tồn tại trong dữ liệu.")
        return pd.DataFrame()
    
    print(f"Lọc các dòng có rủi ro trầm cảm 'High' hoặc 'Very High' trong cột '{column}'.")
    filtered_data = data[data[column].isin(['High', 'Very High'])]
    
    # Lưu trữ dữ liệu lọc vào một file CSV để tiến hành vẽ biểu đồ
    filtered_data.to_csv("filtered_depression_data.csv", index=False)
    print("Đã lưu trữ dữ liệu vào file filtered_depression_data.csv ")
    return filtered_data

# Đọc dữ liệu từ file CSV và thực hiện lọc theo nguy cơ trầm cảm
if __name__ == "__main__":
    data = read_csv_data()
    if not data.empty:
        filtered_data = filter_depression_risk(data)
        

