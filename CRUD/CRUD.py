import csv
import pandas as pd
import math

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

# Tải dữ liệu từ file CSV
def load_data():
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader]
    except FileNotFoundError:
        return []

# Lưu dữ liệu vào file CSV
def save_data(data):
    with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(data)

# Hiển thị dữ liệu với phân trang
def display_data(data, page_size=4):
    total_pages = math.ceil(len(data) / page_size)
    page = 1

    while True:
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        subset = data[start_idx:end_idx]

        # Hiển thị dưới dạng bảng
        print(pd.DataFrame(subset))
        print(f"Trang {page}/{total_pages}")

        # Điều hướng phân trang
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

# Tạo dữ liệu mới
def create_data(data):
    try:
        new_entry = {}
        for field in FIELD_NAMES:
            value = input(f"Nhập {field}: ").strip()
            new_entry[field] = value

        data.append(new_entry)
        save_data(data)
        print("Thêm dữ liệu thành công!")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ!")

# Cập nhật dữ liệu
def update_data(data):
    try:
        update_name = input("Nhập tên (Name) của dòng muốn cập nhật: ").strip()
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

# Xóa dữ liệu
def delete_data(data):
    try:
        delete_names = input("Nhập tên (Name) các dòng muốn xóa (phân cách bằng dấu phẩy): ").strip()
        delete_names = delete_names.split(',')

        data[:] = [item for item in data if item["Name"] not in delete_names]
        save_data(data)
        print("Xóa dữ liệu thành công!")
    except ValueError:
        print("Dữ liệu nhập không hợp lệ!")

# Chương trình chính
def main():
    data = load_data()

    while True:
        print("\nMenu:")
        print("1. Hiển thị danh sách dữ liệu")
        print("2. Tạo dữ liệu mới")
        print("3. Cập nhật dữ liệu")
        print("4. Xóa dữ liệu")
        print("5. Thoát")

        choice = input("Lựa chọn: ").strip()
        if choice == '1':
            display_data(data)
        elif choice == '2':
            create_data(data)
        elif choice == '3':
            update_data(data)
        elif choice == '4':
            delete_data(data)
        elif choice == '5':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
