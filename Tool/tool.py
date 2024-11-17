import pandas as pd
from tabulate import tabulate

def load_csv(file_path):
    """
    Đọc dữ liệu từ tệp CSV và trả về DataFrame.
    """
    return pd.read_csv(file_path)

def sort_data(data, columns, order):
    """
    Sắp xếp dữ liệu theo các cột cụ thể với thứ tự riêng cho từng cột.
    """
    return data.sort_values(by=columns, ascending=order)

def search_data(data, column, value):
    """
    Tìm kiếm các hàng trong một cột có chứa giá trị cụ thể.
    """
    return data[data[column].astype(str).str.contains(value, case=False)]

def filter_data(data, column, condition):
    """
    Lọc dữ liệu dựa trên điều kiện cụ thể cho một cột.
    """
    return data.query(f"{column} {condition}")

def display_data(data, page_size=10):
    """
    Hiển thị dữ liệu dưới dạng bảng với hỗ trợ phân trang.

    Args:
        data (pandas.DataFrame): Dữ liệu cần hiển thị.
        page_size (int): Số hàng hiển thị trên mỗi trang.
    """
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

def main():
    """
    Chương trình chính: Đọc dữ liệu từ tệp CSV và cho phép người dùng 
    sắp xếp, tìm kiếm, lọc hoặc hiển thị dữ liệu với hỗ trợ phân trang.
    """
    file_path = r"C:\Users\HoangDuc\Downloads\cleaned_and_predicted_data.csv"
    data = load_csv(file_path)
    
    while True:
        print("\nChọn chức năng:")
        print("1. Hiển thị dữ liệu")
        print("2. Sắp xếp dữ liệu")
        print("3. Tìm kiếm dữ liệu")
        print("4. Lọc dữ liệu")
        print("5. Thoát")
        choice = input("Lựa chọn: ")
        
        if choice == '1':
            page_size = int(input("Nhập số hàng mỗi trang (mặc định 10): ") or 10)
            display_data(data, page_size=page_size)
        
        elif choice == '2':
            columns = input("Nhập tên cột cần sắp xếp (ngăn cách bằng dấu phẩy): ").split(",")
            order = []
            for col in columns:
                col_order = input(f"Sắp xếp cột '{col}' tăng dần? (y/n): ").lower() == 'y'
                order.append(col_order)
            data = sort_data(data, columns, order)
            print("Dữ liệu đã được sắp xếp.")
        
        elif choice == '3':
            column = input("Nhập tên cột cần tìm kiếm: ")
            value = input("Nhập giá trị cần tìm: ")
            result = search_data(data, column, value)
            display_data(result)
        
        elif choice == '4':
            column = input("Nhập tên cột cần lọc: ")
            condition = input("Nhập điều kiện lọc (ví dụ: '== \"Divorced\"'): ")
            result = filter_data(data, column, condition)
            display_data(result)
        
        elif choice == '5':
            break
        
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
