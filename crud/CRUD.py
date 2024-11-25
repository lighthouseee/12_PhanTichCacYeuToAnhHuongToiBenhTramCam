import csv

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

# Đọc dữ liệu từ file CSV
def read_csv_data():
    try:
        with open(CSV_FILE, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader]
    except FileNotFoundError:
        return []

def paginate_data(data, page_size):
    """
    Phân trang dữ liệu và xử lý điều hướng giữa các trang.
    :param data: DataFrame
    :param page_size: Số dòng mỗi trang
    """
    total_pages = (len(data) + page_size - 1) // page_size  # Tính tổng số trang
    current_page = 1
    line_width = 175

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
