import pandas as pd
import numpy as np

# Đọc file CSV
file_path = 'depression_data.csv'  
data = pd.read_csv(file_path)

# Hiển thị thông tin tổng quan ban đầu
print("Một vài dòng dữ liệu:\n", data.head())

# ----- Mô tả các giá trị hợp lệ cho từng trường dữ liệu -----
def describe_valid_values(df):
    """
    Mô tả các giá trị hợp lệ cho từng trường dữ liệu trong DataFrame.

    Args:
        df (pd.DataFrame): Dữ liệu cần kiểm tra.

    Returns:
        None: In ra mô tả cho từng trường.
    """
    for col in df.columns:
        print(f"Trường dữ liệu: {col}")
        
        if df[col].dtype == 'object':
            # Các cột kiểu chuỗi
            unique_values = df[col].dropna().unique()
            print(f"  Kiểu dữ liệu hợp lệ: Chuỗi")
            print(f"  Các giá trị hợp lệ có thể bao gồm: {unique_values[:10]} ...")  # In ra một vài giá trị hợp lệ
        elif df[col].dtype in ['int64', 'float64']:
            # Các cột kiểu số
            if col == 'Age':
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên trong khoảng từ 0 đến 120")
            elif col == 'Income':
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên hoặc số thực, giá trị không âm")
            elif col == 'Physical Activity Level':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'")
            elif col == 'Smoking Status':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Smoker', 'Non-Smoker'")
            elif col == 'History of Mental Illness':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Yes', 'No'")
            elif col == 'Chronic Medical Conditions':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Yes', 'No'")
            elif col == 'Sleep Patterns':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Poor', 'Average', 'Good', 'Very Good'")
            else:
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên hoặc số thực")
        else:
            print(f"  Không xác định được kiểu dữ liệu hợp lệ.")
        
        print("\n")

# Gọi hàm mô tả các giá trị hợp lệ
describe_valid_values(data)

# ----- Bước 1: Phân tích dữ liệu -----
# 1. Kiểm tra giá trị bất thường
def detect_outliers(df):
    """
    Phát hiện giá trị bất thường trong dữ liệu.

    Args:
        df (pd.DataFrame): Dữ liệu cần kiểm tra.

    Returns:
        dict: Từ điển chứa các cột có giá trị bất thường và mô tả vấn đề.
    """
    issues = {}
    # Kiểm tra tuổi (Age)
    if (df['Age'] < 0).any() or (df['Age'] > 120).any():
        issues['Age'] = "Tuổi bất hợp lệ (âm hoặc lớn hơn 120)."
    # Kiểm tra thu nhập (Income)
    if (df['Income'] < 0).any():
        issues['Income'] = "Thu nhập âm."
    return issues

outliers = detect_outliers(data)
print("\nCác vấn đề bất thường:\n", outliers)

# 2. Kiểm tra dữ liệu thiếu (missing values)
missing_values = data.isnull().sum()
print("\nSố lượng giá trị thiếu trong từng cột:\n", missing_values)

# ----- Bước 2: Làm sạch dữ liệu -----
# 1. Xử lý giá trị bất thường
data = data[(data['Age'] >= 0) & (data['Age'] <= 120)]  # Loại bỏ tuổi bất hợp lệ
data = data[data['Income'] >= 0]  # Loại bỏ thu nhập âm

# 3. Điền giá trị thiếu
for col in data.columns:
    if data[col].dtype in ['int64', 'float64']:
        # Điền giá trị trung bình cho cột số
        data[col].fillna(data[col].mean())
    else:
        # Điền "Unknown" cho cột chuỗi
        data[col].fillna('Unknown')

# 4. Chuẩn hóa dữ liệu
# Loại bỏ khoảng trắng thừa ở cột chuỗi
for col in data.select_dtypes(include=['object']).columns:
    data[col] = data[col].str.strip()

# ----- Bước 3: Phát sinh dữ liệu mới -----
# Tạo cột "Depression Risk" - Đây là cột dự đoán xem một người có khả năng dẫn đến trầm cảm hay không dựa trên các điều kiện khách quan
def predict_depression_risk(row):
    """
    Dự đoán mức độ trầm cảm dựa trên các yếu tố trong dữ liệu.

    Args:
        row (pd.Series): Một dòng dữ liệu.

    Returns:
        str: Mức độ trầm cảm: 'Very High', 'High', 'Medium', 'Low', 'Very Low'.
    """
    risk_score = 0

    # Thu nhập thấp (dưới 20,000)
    if row['Income'] < 20000:
        risk_score += 1
    
    # Tình trạng hoạt động thể chất ít (Sedentary)
    if row['Physical Activity Level'] == 'Sedentary':
        risk_score += 1
    
    # Hút thuốc
    if row['Smoking Status'] == 'Smoker':
        risk_score += 1
    
    # Tiền sử bệnh tâm lý
    if row['History of Mental Illness'] == 'Yes':
        risk_score += 1
    
    # Bệnh lý mãn tính
    if row['Chronic Medical Conditions'] == 'Yes':
        risk_score += 1
    
    # Ngủ kém (Poor)
    if row['Sleep Patterns'] == 'Poor':
        risk_score += 1
        
    # Kiểm tra số lượng con có nhiều quá hay không
    if row['Number of Children'] >= 3:
        risk_score += 1  
        
    # Kiểm tra tình trạng thất nghiệp
    if row['Employment Status'] == 'Unemployed':
        risk_score += 1  
        
    # Phân loại mức độ trầm cảm dựa trên điểm số
    if risk_score >= 5:
        return 'Very High'
    elif risk_score == 4:
        return 'High'
    elif risk_score == 3:
        return 'Medium'
    elif risk_score == 2:
        return 'Low'
    else:
        return 'Very Low'

# Áp dụng hàm dự đoán mức độ trầm cảm vào từng dòng dữ liệu
data['Depression Risk'] = data.apply(predict_depression_risk, axis=1)

# ----- Kết quả -----
# Thông tin sau khi làm sạch và thêm cột "Depression Risk"
print("\nDữ liệu sau khi làm sạch và thêm cột Depression Risk:\n")
print(data[['Age', 'Income', 'Physical Activity Level', 'Smoking Status', 'History of Mental Illness', 'Chronic Medical Conditions', 'Sleep Patterns', 'Depression Risk']].head())

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'cleaned_and_predicted_data.csv'
data.to_csv(output_path, index=False)
print(f"\nDữ liệu đã được lưu vào file '{output_path}'.")
