<<<<<<< Updated upstream:CRUD/CRUD.py
import csv
=======
import pandas as pd
import math
>>>>>>> Stashed changes:crud/CRUD.py

CSV_FILE = "cleaned_and_predicted_data.csv"

<<<<<<< Updated upstream:CRUD/CRUD.py
# Định nghĩa các cột
FIELD_NAMES = [
    "Name", "Age", "Marital Status", "Education Level", "Number of Children", 
    "Smoking Status", "Physical Activity Level", "Employment Status", "Income", 
    "Alcohol Consumption", "Dietary Habits", "Sleep Patterns", 
    "History of Mental Illness", "History of Substance Abuse", 
    "Family History of Depression", "Chronic Medical Conditions"
]

# Đọc dữ liệu từ file CSV
def read_csv_data():
=======
def read_csv_data():
    """
    Đọc dữ liệu từ file CSV và trả về DataFrame.
    """
>>>>>>> Stashed changes:crud/CRUD.py
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader]
    except FileNotFoundError:
<<<<<<< Updated upstream:CRUD/CRUD.py
        return []

def paginate_data(data, page_size):
=======
        return pd.DataFrame()

def paginate_data(data, page_size, current_page):
>>>>>>> Stashed changes:crud/CRUD.py
    """
    Phân trang dữ liệu.
    :param data: DataFrame hiện tại
    :param page_size: Số dòng mỗi trang
    :param current_page: Trang hiện tại
    :return: DataFrame của trang hiện tại và tổng số trang
    """
    total_pages = math.ceil(len(data) / page_size)
    if current_page < 1 or current_page > total_pages:
        raise ValueError("Trang không hợp lệ.")
    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    return data.iloc[start_idx:end_idx], total_pages

<<<<<<< Updated upstream:CRUD/CRUD.py
    while True:
        # Lấy dữ liệu của trang hiện tại
        start_idx = (current_page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = data.iloc[start_idx:end_idx]

        # Hiển thị dữ liệu
        print(paginated_data)
        
        # Canh giữa cho số trang
        page_info = f"Trang {current_page}/{total_pages}"
        padding = (line_width - len(page_info)) // 2
        print("\n" + " " * padding + page_info + " " * padding + "\n")
        print(" " * line_width)

        # Điều hướng giữa các trang
        if total_pages > 1:
            action = input("Nhập 'n' để sang trang, 'p' để quay lại, hoặc 'q' để thoát: ").strip().lower()
            if action == "n" and current_page < total_pages:
                current_page += 1
            elif action == "p" and current_page > 1:
                current_page -= 1
            elif action == "q":
                print("Thoát phân trang.")
                break
            else:
                print("Lựa chọn không hợp lệ!")
        else:
            print("Không có thêm trang nào.")
            break

# Lưu dữ liệu vào file CSV
def save_data(data):
    with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerows(data)

# Tạo dữ liệu mới
def create_data(data, new_entry):
    data.append(new_entry)
    save_data(data)

# Cập nhật dữ liệu
def update_data(data, target_name, updated_entry):
    record = next((item for item in data if item["Name"] == target_name), None)
    if record:
        record.update(updated_entry)
        save_data(data)
        return True
    return False

# Xóa dữ liệu
def delete_data(data, target_names):
    initial_count = len(data)
    data[:] = [item for item in data if item["Name"] not in target_names]
    save_data(data)
    return len(data) < initial_count
=======
def create_data(data, new_entry):
    """
    Thêm một bản ghi mới vào DataFrame và lưu vào CSV.
    :param data: DataFrame hiện tại
    :param new_entry: Dữ liệu mới dạng dictionary
    :return: DataFrame đã cập nhật
    """
    # Tạo DataFrame từ bản ghi mới
    new_data = pd.DataFrame([new_entry])

    # Thêm bản ghi mới vào file CSV (append mode)
    new_data.to_csv(CSV_FILE, mode='a', index=False, header=False)

    # Cập nhật DataFrame hiện tại
    updated_data = pd.concat([data, new_data], ignore_index=True)
    return updated_data

def update_data(data, target_name, updated_entry):
    """
    Cập nhật dữ liệu của một bản ghi cụ thể dựa trên tên.
    :param data: DataFrame hiện tại
    :param target_name: Giá trị Name của bản ghi cần cập nhật
    :param updated_entry: Dữ liệu cập nhật dưới dạng dictionary
    :return: True nếu cập nhật thành công, False nếu không tìm thấy bản ghi
    """
    # Tìm chỉ số của bản ghi cần cập nhật
    record_index = data.index[data["Name"] == target_name]

    # Nếu tìm thấy bản ghi
    if not record_index.empty:
        for col, value in updated_entry.items():
            data.at[record_index[0], col] = value  # Cập nhật giá trị mới cho từng cột

        # Lưu dữ liệu đã cập nhật vào file CSV
        data.to_csv(CSV_FILE, index=False)
        return True

    # Nếu không tìm thấy bản ghi
    return False
>>>>>>> Stashed changes:crud/CRUD.py
