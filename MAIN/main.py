import csv
import pandas as pd
import math
from tabulate import tabulate

# Đường dẫn file CSV
CSV_FILE = "cleaned_and_predicted_data.csv"

# Định nghĩa các cột
FIELD_NAMES = [
    "Name", "Age", "Marital Status", "Education Level", "Number of Children", 
    "Smoking Status", "Physical Activity Level", "Employment Status", "Income", 
    "Alcohol Consumption", "Dietary Habits", "Sleep Patterns", 
    "History of Mental Illness", "History of Substance Abuse", 
    "Family History of Depression", "Chronic Medical Conditions"
]

# CRUD Functions
def load_data():
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader]
    except FileNotFoundError:
        return []

def save_data(data):
    with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(data)

def display_data(data, page_size=10):
    total_pages = math.ceil(len(data) / page_size)
    page = 1

    while True:
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        subset = data[start_idx:end_idx]
        print(pd.DataFrame(subset))
        print(f"Trang {page}/{total_pages}")

        print("Nhập 'n' để trang tiếp theo, 'p' để quay lại, hoặc 'q' để thoát.")
        choice = input("Lựa chọn: ").strip().lower()

        if choice == 'n' and page < total_pages:
            page += 1
        elif choice == 'p' and page > 1:
            page -= 1
        elif choice == 'q':
            break
        else:
            print("Lựa chọn không hợp lệ!")

def create_data(data):
    try:
        create_name = input("Lưu ý khi nhập dữ liệu mới phải nhập cả họ tên(bấm ENTER để tiếp tục). ")
        new_entry = {}
        for field in FIELD_NAMES:
            value = input(f"Nhập {field}: ").strip()
            new_entry[field] = value

        data.append(new_entry)
        save_data(data)
        print("Thêm dữ liệu thành công!")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ!")

def update_data(data):
    try:
        update_name = input("Nhập tên (Name) của dòng muốn cập nhật (Lưu ý: khi cập nhập tên phải nhập cả họ tên): ").strip()
        record = next((item for item in data if item["Name"] == update_name), None)

        if record:
            print(f"Dữ liệu hiện tại: {record}")
            for field in FIELD_NAMES:
                new_value = input(f"Nhập {field} mới (hoặc Enter để giữ nguyên): ").strip()
                if new_value:
                    record[field] = new_value
            save_data(data)
            print("Cập nhật thành công!")
        else:
            print("Không tìm thấy dòng dữ liệu với tên đã nhập.")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ!")

def delete_data(data):
    try:
        delete_names = input("Nhập tên (Name) các dòng muốn xóa (phân cách bằng dấu phẩy và xóa phải nhập đầy đủ họ tên): ").strip()
        delete_names = delete_names.split(',')

        data[:] = [item for item in data if item["Name"] not in delete_names]
        save_data(data)
        print("Xóa dữ liệu thành công!")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ!")

# Tool Functions
def load_csv(file_path):
    return pd.read_csv(file_path)

def sort_data(data, columns, order):
    return data.sort_values(by=columns, ascending=order)

def search_data(data, column, value):
    return data[data[column].astype(str).str.contains(value, case=False)]

def filter_data(data, column, condition):
    return data.query(f"{column} {condition}")

def filter_depression_risk(data):
    return data[data['Depression Risk'].isin(['High', 'Very High'])]

def display_tool_data(data, page_size=10):
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

# Main Menu
def main():
    data = load_data()

    while True:
        print("\nChọn chức năng:")
        print("1. CRUD")
        print("2. Tool")
        print("3. Thoát")

        choice = input("Lựa chọn: ").strip()

        if choice == '1':
            while True:
                print("\nCRUD - Chọn chức năng:")
                print("1. Hiển thị dữ liệu")
                print("2. Tạo dữ liệu")
                print("3. Cập nhật dữ liệu")
                print("4. Xóa dữ liệu")
                print("5. Quay lại menu chính")

                crud_choice = input("Lựa chọn: ").strip()

                if crud_choice == '1':
                    display_data(data)
                elif crud_choice == '2':
                    create_data(data)
                elif crud_choice == '3':
                    update_data(data)
                elif crud_choice == '4':
                    delete_data(data)
                elif crud_choice == '5':
                    break
                else:
                    print("Lựa chọn không hợp lệ!")

        elif choice == '2':
            while True:
                print("\nTool - Chọn chức năng:")
                print("1. Lọc dữ liệu theo mức độ nguy cơ trầm cảm")
                print("2. Tìm kiếm dữ liệu")
                print("3. Sắp xếp dữ liệu")
                print("4. Quay lại menu chính")

                tool_choice = input("Lựa chọn: ").strip()

                if tool_choice == '1':
                    file_path = input("Nhập đường dẫn file CSV: ").strip()
                    data = load_csv(file_path)
                    filtered_data = filter_depression_risk(data)
                    display_tool_data(filtered_data)
                elif tool_choice == '2':
                    column = input("Nhập tên cột cần tìm kiếm: ").strip()
                    value = input("Nhập giá trị cần tìm: ").strip()
                    result = search_data(data, column, value)
                    display_tool_data(result)
                elif tool_choice == '3':
                    columns = input("Nhập tên cột để sắp xếp (cách nhau bằng dấu phẩy): ").strip().split(',')
                    order = input("Nhập thứ tự sắp xếp (asc/desc): ").strip() == 'asc'
                    sorted_data = sort_data(data, columns, order)
                    display_tool_data(sorted_data)
                elif tool_choice == '4':
                    break
                else:
                    print("Lựa chọn không hợp lệ!")

        elif choice == '3':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()

