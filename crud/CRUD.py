import pandas as pd
import math

CSV_FILE = "cleaned_and_predicted_data.csv"

# Định nghĩa các cột
FIELD_NAMES = [
    "Name", "Age", "Marital Status", "Education Level", "Number of Children", 
    "Smoking Status", "Physical Activity Level", "Employment Status", "Income", 
    "Alcohol Consumption", "Dietary Habits", "Sleep Patterns", 
    "History of Mental Illness", "History of Substance Abuse", 
    "Family History of Depression", "Chronic Medical Conditions"
]

def read_csv_data():
    """
    Đọc dữ liệu từ file CSV và đặt chỉ số bắt đầu từ 1.
    :return: DataFrame với chỉ số bắt đầu từ 1
    """
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=FIELD_NAMES)

def read_csv_data():
    """
    Đọc dữ liệu từ file CSV và trả về DataFrame.
    """
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame()

# Lưu dữ liệu vào file CSV
def save_data(data):
    data.to_csv(CSV_FILE, index=False)
    
def paginate_data(data, page_size, current_page):
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

def delete_records(data, indices):
    """
    Xóa các bản ghi từ DataFrame dựa trên danh sách chỉ số.
    """
    try:
        # Xóa các bản ghi khỏi DataFrame
        data = data.drop(indices).reset_index(drop=True)
        # Ghi lại vào file CSV
        data.to_csv(CSV_FILE, index=False)
        return data
    except Exception as e:
        raise ValueError(f"Đã xảy ra lỗi khi xóa dữ liệu: {e}")

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

# Xóa dữ liệu
def delete_data(data, target_names):
    # Lấy số lượng bản ghi ban đầu
    initial_count = len(data)
    
    # Loại bỏ các bản ghi có tên trong `target_names`
    data = data[~data["Name"].isin(target_names)]
    
    # Lưu dữ liệu sau khi xóa
    save_data(data)
    
    # Trả về True nếu đã xóa ít nhất một bản ghi
    return len(data) < initial_count

    # Lấy số lượng bản ghi ban đầu
    initial_count = len(data)
    
    # Loại bỏ các bản ghi có tên trong `target_names`
    data = data[~data["Name"].isin(target_names)]
    
    # Lưu dữ liệu sau khi xóa
    save_data(data)
    
    # Trả về True nếu đã xóa ít nhất một bản ghi
    return len(data) < initial_count