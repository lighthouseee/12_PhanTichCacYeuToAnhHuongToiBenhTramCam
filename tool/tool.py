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
def display_column(data):
    column_mapping = {str(i + 1): col for i, col in enumerate(data.columns)}
    print("\nDanh sách các cột hiện có trong dữ liệu:")
    for idx, col in column_mapping.items():
        print(f"{idx}. {col}")
    return column_mapping

# Hiển thị giá trị duy nhất trong một cột
def display_column_values(data, column):
    """
    Hiển thị các giá trị duy nhất trong cột và trả về mapping giữa số thứ tự và giá trị.
    """
    unique_values = sorted(data[column].dropna().unique())
    value_mapping = {str(i + 1): val for i, val in enumerate(unique_values)}
    print(f"\nCột '{column}' có các giá trị:")
    for num, val in value_mapping.items():
        print(f"{num}. {val}")
    return value_mapping

# Chọn cột từ danh sách
def choose_columns(data):
    column_mapping = display_column(data)
    while True:
        selected_numbers = input("Nhập số thứ tự của các cột muốn chọn (cách nhau bởi dấu cách): ").strip().split()
        if all(num in column_mapping for num in selected_numbers):
            return [column_mapping[num] for num in selected_numbers]
        else:
            print("Lỗi: Có cột không hợp lệ. Vui lòng thử lại.")

def sort_data(data):
    """
    Sắp xếp dữ liệu theo nhiều cột, với tùy chọn tăng hoặc giảm cho từng cột.
    Hỗ trợ sắp xếp tiếp tục.
    """
    while True:
        print("\n--- BẮT ĐẦU SẮP XẾP ---")
        column_mapping = display_column(data)  # Hiển thị danh sách cột để chọn

        selected_columns = []
        sort_orders = []

        # Chọn nhiều cột để sắp xếp
        while True:
            selected_numbers = input("Nhập số thứ tự của các cột muốn sắp xếp (cách nhau bởi dấu cách): ").strip().split()
            if all(num in column_mapping for num in selected_numbers):
                selected_columns = [column_mapping[num] for num in selected_numbers]
                break
            else:
                print("Lỗi: Có cột không hợp lệ. Vui lòng thử lại.")

        # Xác định thứ tự sắp xếp (tăng hoặc giảm) cho từng cột
        for column in selected_columns:
            while True:
                order = input(f"Thứ tự sắp xếp cho cột '{column}' (tăng? y/n): ").strip().lower()
                if order in ["y", "n"]:
                    sort_orders.append(order == "y")
                    break
                else:
                    print("Lỗi: Vui lòng nhập 'y' cho tăng hoặc 'n' cho giảm.")

        # Thực hiện sắp xếp
        print(f"\nSắp xếp dữ liệu theo các cột: {selected_columns} với thứ tự {'tăng' if all(sort_orders) else 'hỗn hợp'}.")
        data = data.sort_values(by=selected_columns, ascending=sort_orders)
        print("Dữ liệu đã được sắp xếp thành công.")

        # Hỏi người dùng có muốn sắp xếp thêm không
        choice = input("\nBạn có muốn sắp xếp tiếp không? (y/n): ").strip().lower()
        if choice != 'y':
            print("Quay về menu chính.")
            break

    return data

# Hàm lọc dữ liệu
def filter_data(data):
    """
    Lọc dữ liệu theo điều kiện từ một hoặc nhiều cột.
    Chỉ in ra tên và các cột đã lọc.
    """
    filtered_data = data.copy()  # Khởi tạo biến filtered_data từ data gốc
    selected_columns = []  # Lưu trữ các cột đã được lọc

    while True:
        print("\n--- BẮT ĐẦU LỌC ---")
        column_mapping = display_column(filtered_data)  # Hiển thị danh sách các cột

        # Chọn nhiều cột
        while True:
            selected_numbers = input("Nhập số thứ tự của các cột muốn lọc (cách nhau bởi dấu cách): ").strip().split()
            if all(num in column_mapping for num in selected_numbers):
                selected_columns.extend([column_mapping[num] for num in selected_numbers])
                break
            else:
                print("Lỗi: Có cột không hợp lệ. Vui lòng thử lại.")

        # Lọc lần lượt từng cột
        for column in selected_columns:
            print(f"\n--- Lọc dữ liệu trong cột '{column}' ---")

            if pd.api.types.is_numeric_dtype(filtered_data[column]):
                # Xử lý dữ liệu số
                print(f"\nNhập điều kiện lọc cho cột '{column}' (ví dụ: > 50, <= 100, == 25):")
                while True:
                    condition = input("Điều kiện: ").strip()
                    try:
                        filtered_data = filtered_data.query(f"`{column}` {condition}")
                        print(f"Dữ liệu sau khi lọc cột '{column}' còn {len(filtered_data)} dòng.")
                        break
                    except Exception as e:
                        print(f"Lỗi: Điều kiện không hợp lệ ({e}). Vui lòng nhập lại.")
            else:
                # Xử lý dữ liệu chuỗi
                unique_values = sorted(filtered_data[column].dropna().unique())
                value_mapping = {str(i + 1): val for i, val in enumerate(unique_values)}
                print(f"\nCột '{column}' có các giá trị khả dụng:")
                for num, val in value_mapping.items():
                    print(f"{num}. {val}")

                print("\nNhập số tương ứng với giá trị cần lọc (có thể nhập nhiều, cách nhau bởi dấu cách):")
                while True:
                    selected_numbers = input("Số thứ tự: ").strip().split()
                    if all(num in value_mapping for num in selected_numbers):
                        selected_values = [value_mapping[num] for num in selected_numbers]
                        filtered_data = filtered_data[filtered_data[column].isin(selected_values)]
                        print(f"Dữ liệu sau khi lọc cột '{column}' còn {len(filtered_data)} dòng.")
                        break
                    else:
                        print("Lỗi: Có giá trị không hợp lệ. Vui lòng thử lại.")

        # Hỏi người dùng có muốn tiếp tục lọc không
        choice = input("\nBạn có muốn tiếp tục lọc không? (y/n): ").strip().lower()
        if choice != 'y':
            print("Kết thúc quá trình lọc.")
            break

    # Chỉ hiển thị tên và các cột đã lọc
    display_columns = ['Name'] + selected_columns
    return filtered_data[display_columns]


# Hàm tìm kiếm dữ liệu
def search_data(data):
    """
    Tìm kiếm các dòng chứa giá trị cụ thể trong một hoặc nhiều cột.
    Chỉ in ra tên và các cột đã tìm kiếm.
    """
    filtered_data = data.copy()
    selected_columns = []  # Lưu trữ các cột đã được tìm kiếm

    while True:
        print("\n--- BẮT ĐẦU TÌM KIẾM ---")
        column_mapping = display_column(filtered_data) 

        # Chọn nhiều cột
        while True:
            selected_numbers = input("Nhập số thứ tự của các cột muốn tìm kiếm (cách nhau bởi dấu cách): ").strip().split()
            if all(num in column_mapping for num in selected_numbers):
                selected_columns.extend([column_mapping[num] for num in selected_numbers])
                break
            else:
                print("Lỗi: Có cột không hợp lệ. Vui lòng thử lại.")

        # Tìm kiếm lần lượt trong từng cột
        for column in selected_columns:
            print(f"\n--- Tìm kiếm trong cột '{column}' ---")

            # Hiển thị giá trị khả dụng trong cột
            unique_values = sorted(filtered_data[column].dropna().unique())
            value_mapping = {str(i + 1): val for i, val in enumerate(unique_values)}
            print(f"Cột '{column}' có các giá trị khả dụng:")
            for num, val in value_mapping.items():
                print(f"{num}. {val}")

            print("\nNhập số tương ứng với các giá trị cần tìm kiếm (cách nhau bởi dấu cách):")
            while True:
                search_inputs = input("Số thứ tự: ").strip().split()

                # Kiểm tra hợp lệ của các số thứ tự
                if all(input_num in value_mapping for input_num in search_inputs):
                    search_values = [value_mapping[input_num] for input_num in search_inputs]
                    break
                else:
                    print("Lỗi: Có số thứ tự không hợp lệ. Vui lòng chọn lại từ danh sách.")

            # Lọc dữ liệu theo các giá trị đã chọn
            filtered_data = filtered_data[filtered_data[column].isin(search_values)]
            if filtered_data.empty:
                print(f"Không tìm thấy giá trị nào trong cột '{column}' với các lựa chọn {search_values}.")
                break
            else:
                print(f"Tìm thấy {len(filtered_data)} dòng phù hợp với các giá trị {search_values} trong cột '{column}'.")

        # Hỏi người dùng có muốn tiếp tục tìm kiếm không
        choice = input("\nBạn có muốn tiếp tục tìm kiếm không? (y/n): ").strip().lower()
        if choice != 'y':
            print("Kết thúc tìm kiếm.")
            break

    # Chỉ hiển thị tên và các cột đã tìm kiếm
    display_columns = ['Name'] + selected_columns
    return filtered_data[display_columns]

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
