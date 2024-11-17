import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

def sort_data(data, columns, ascending=True):
    return data.sort_values(by=columns, ascending=ascending)

def search_data(data, column, value):
    return data[data[column].astype(str).str.contains(value, case=False)]

def filter_data(data, column, condition):
    return data.query(f"{column} {condition}")

def main():
    file_path = r"C:\Users\HoangDuc\Downloads\cleaned_and_predicted_data.csv"
    data = load_csv(file_path)
    
    while True:
        print("\nChọn chức năng:")
        print("1. Sắp xếp dữ liệu")
        print("2. Tìm kiếm dữ liệu")
        print("3. Lọc dữ liệu")
        print("4. Thoát")
        choice = input("Lựa chọn: ")
        
        if choice == '1':
            columns = input("Nhập tên cột cần sắp xếp (ngăn cách bằng dấu phẩy): ").split(",")
            order = input("Sắp xếp tăng dần? (y/n): ").lower() == 'y'
            result = sort_data(data, columns, ascending=order)
            print(result)
        
        elif choice == '2':
            column = input("Nhập tên cột cần tìm kiếm: ")
            value = input("Nhập giá trị cần tìm: ")
            result = search_data(data, column, value)
            print(result)
        
        elif choice == '3':
            column = input("Nhập tên cột cần lọc: ")
            condition = input("Nhập điều kiện lọc (ví dụ: '== \"Divorced\"'): ")
            result = filter_data(data, column, condition)
            print(result)
        
        elif choice == '4':
            break
        
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
