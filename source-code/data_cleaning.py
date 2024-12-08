import pandas as pd
import numpy as np

# Đọc file CSV
file_path = 'dataset\\depression_data.csv'  
data = pd.read_csv(file_path)

def remove_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Loại bỏ giá trị không hợp lệ (outliers) trong DataFrame bằng cách thay thế chúng bằng NaN.
    Điều kiện loại bỏ được định nghĩa cho cả dữ liệu số và chuỗi.
    """
    # Điều kiện lọc với dữ liệu số
    num_conditions = {
        'Age': (data['Age'] >= 18) & (data['Age'] <= 80), 
        'Income': data['Income'] >= 0,
        'Number of Children': data['Number of Children'] >= 0
    }

    # Điều kiện lọc với dữ liệu chuỗi
    cat_conditions = {
        'Physical Activity Level': data['Physical Activity Level'].isin(['Sedentary', 'Moderate', 'Active']),
        'Smoking Status': data['Smoking Status'].isin(['Non-smoker', 'Former', 'Current']),
        'Employment Status': data['Employment Status'].isin(['Employed', 'Unemployed']),
        'Alcohol Consumption': data['Alcohol Consumption'].isin(['Low', 'Moderate', 'High']),
        'Dietary Habits': data['Dietary Habits'].isin(['Healthy', 'Moderate', 'Unhealthy']),
        'Sleep Patterns': data['Sleep Patterns'].isin(['Poor', 'Good', 'Fair']),
        'History of Mental Illness': data['History of Mental Illness'].isin(['Yes', 'No']),
        'Family History of Depression': data['Family History of Depression'].isin(['Yes', 'No']),
        'Chronic Medical Conditions': data['Chronic Medical Conditions'].isin(['Yes', 'No']),
        'Marital Status': data['Marital Status'].isin(['Single', 'Married', 'Divorced', 'Widowed']),
        'Education Level': data['Education Level'].isin(["High School", "Bachelor's Degree", "Master's Degree", "Associate Degree", "PhD"])
    }

    # Thay thế các giá trị không thỏa mãn điều kiện bằng NaN
    for column, condition in num_conditions.items():
        if column in data.columns:
            data.loc[~condition, column] = np.nan

    for column, condition in cat_conditions.items():
        if column in data.columns:
            data.loc[~condition, column] = np.nan

    return data

def fill_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Điền các giá trị thiếu trong DataFrame.
    """

    # Xử lý các cột số
    num_columns = data.select_dtypes(include=['number']).columns
    if not num_columns.empty:
        skewness = data[num_columns].skew().abs()
        median_cols = skewness[skewness > 1].index  # Cột có độ lệch lớn
        mean_cols = skewness[skewness <= 1].index  # Cột có độ lệch nhỏ

        # Điền trung vị (median) cho các cột lệch
        for col in median_cols:
            if col in data.columns:
                median_value = data[col].median()
                data[col] = data[col].fillna(round(median_value)).astype(int)

        # Điền trung bình (mean) cho các cột không lệch 
        for col in mean_cols:
            if col in data.columns:
                mean_value = data[col].mean()
                data[col] = data[col].fillna(round(mean_value)).astype(int)

    # Xử lý các cột chuỗi
    no_fill = {
        'History of Mental Illness': 'No',
        'History of Substance Abuse': 'No',
        'Family History of Depression': 'No',
        'Chronic Medical Conditions': 'No',
    }
    str_columns = data.select_dtypes(include=['object']).columns
    if not str_columns.empty:
        # Điền 'No' với các cột chỉ có 'Yes' hoặc 'No' 
        for col, fill_value in no_fill.items():
            if col in data.columns:
                data[col] = data[col].fillna(fill_value)

        # Điền giá trị xuất hiện nhiều lần nhất cho các cột chuỗi còn lại
        other_cols = str_columns.difference(no_fill.keys())
        if not other_cols.empty:
            modes = data[other_cols].mode().iloc[0]  # Tìm giá trị xuất hiện nhiều lần nhất cho từng cột
            data[other_cols] = data[other_cols].fillna(modes)

    return data

def predict_depression_risk(data: pd.DataFrame) -> pd.Series:
    """
    Dự đoán mức độ trầm cảm dựa trên các yếu tố liên quan trong dữ liệu.
    - Tính điểm rủi ro bằng cách gán điểm cho các điều kiện có nguy cơ cao (ví dụ: thu nhập thấp, lối sống ít vận động, v.v.).
    - Phân loại mức độ rủi ro dựa trên tổng điểm:
    + Very High: Điểm >= 8
    + High: Điểm >= 6
    + Medium: Điểm >= 4
    + Low: Điểm >= 2
    + Very Low: Điểm < 2
    """

    # Tính điểm rủi ro cho các cột
    risk_scores = np.zeros(len(data))

    # Cập nhật điểm rủi ro cho các điều kiện
    risk_scores += (data['Income'] < 20000).astype(int)
    risk_scores += (data['Physical Activity Level'] == 'Sedentary').astype(int)
    risk_scores += (data['Smoking Status'] == 'Current').astype(int)
    risk_scores += (data['History of Mental Illness'] == 'Yes').astype(int)
    risk_scores += (data['Chronic Medical Conditions'] == 'Yes').astype(int)
    risk_scores += (data['Sleep Patterns'] == 'Poor').astype(int)
    risk_scores += (data['Employment Status'] == 'Unemployed').astype(int)
    risk_scores += (data['Alcohol Consumption'] == 'High').astype(int)
    risk_scores += (data['Dietary Habits'] == 'Unhealthy').astype(int)
    risk_scores += (data['History of Substance Abuse'] == 'Yes').astype(int)
    risk_scores += (data['Family History of Depression'] == 'Yes').astype(int)

    # Tạo cột nguy cơ trầm cảm (depression risk) dựa trên risk_scores
    depression_risk = pd.Series(np.select(
        [risk_scores >= 8, risk_scores >= 6, risk_scores >= 4, risk_scores >= 2], 
        ['Very High', 'High', 'Medium', 'Low'], 
        default='Very Low'
    ))

    return depression_risk

# ----- Kết quả ----- 

# Xử lý và làm sạch dữ liệu
cleaned_data = remove_outliers(data)
cleaned_data = fill_missing_values(cleaned_data)

# Tạo cột "Depression Risk" cho toàn bộ dữ liệu
cleaned_data['Depression Risk'] = predict_depression_risk(cleaned_data)
#cleaned_data['Depression Risk'] = predict_depression_risk(cleaned_data)

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'dataset\\cleaned_and_predicted_data.csv'
cleaned_data.to_csv(output_path, index=False)
