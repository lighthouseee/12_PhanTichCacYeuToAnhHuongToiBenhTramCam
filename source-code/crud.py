import pandas as pd
import math

CSV_FILE = "dataset\\cleaned_and_predicted_data.csv"

def read_csv_data():
    """
    Đọc dữ liệu từ file CSV và trả về DataFrame.
    """
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame()

def paginate_data(data: pd.DataFrame, page_size: int, current_page: int):
    """
    Phân trang dữ liệu.
    :param data: DataFrame hiện tại
    :param page_size: Số dòng mỗi trang
    :param current_page: Trang hiện tại
    :return: DataFrame của trang hiện tại và tổng số trang
    """
    # Tính tổng số trang
    total_pages = math.ceil(len(data) / page_size)
    
    # Kiểm tra trang hợp lệ
    if current_page < 1 or current_page > total_pages:
        raise ValueError("Trang không hợp lệ.")
    
    # Tính chỉ số bắt đầu và kết thúc của trang hiện tại
    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    
    # Trả về dữ liệu trang hiện tại và tổng số trang
    return data.iloc[start_idx:end_idx], total_pages


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
    header = not data.empty
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
