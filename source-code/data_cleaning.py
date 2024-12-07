import pandas as pd
import numpy as np

# Đọc file CSV
file_path = 'dataset\\depression_data.csv'  
data = pd.read_csv(file_path)
# def clean_data(file_path: str, output_path: str) -> pd.DataFrame:
#     """
#     Thực hiện việc làm sạch dữ liệu và dự đoán mức độ trầm cảm.
#     """

#     # Đọc file CSV
#     file_path = 'dataset\\depression_data.csv'
#     data = pd.read_csv(file_path)

#     # Xử lý và làm sạch dữ liệu
#     cleaned_data = remove_outliers(data)
#     cleaned_data = fill_missing_values(cleaned_data)

#     # Tạo cột "Depression Risk"
#     cleaned_data['Depression Risk'] = predict_depression_risk(cleaned_data)

#     # Lưu dữ liệu đã làm sạch vào file mới
#     output_path = 'dataset\\cleaned_and_predicted_data.csv'
#     cleaned_data.to_csv(output_path, index=False)

#     return cleaned_data    


def remove_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Thay thế các giá trị bất thường bằng NaN trong DataFrame.
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

    # Chỉ thay thế các giá trị không thỏa mãn điều kiện bằng NaN
    for column, condition in num_conditions.items():
        if column in data.columns:
            data.loc[~condition, column] = np.nan

    for column, condition in cat_conditions.items():
        if column in data.columns:
            data.loc[~condition, column] = np.nan

    return data

def fill_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Điền các giá trị thiếu trong DataFrame
    """
    
    # Xử lý các cột số
    num_columns = data.select_dtypes(include=['number']).columns
    if not num_columns.empty:
        skewness = data[num_columns].skew().abs()
        median_cols = skewness[skewness > 1].index  # Cột có độ lệch lớn
        mean_cols = skewness[skewness <= 1].index  # Cột có độ lệch nhỏ
        
        # Điền median cho các cột lệch
        data[median_cols] = data[median_cols].fillna(data[median_cols].median()).round(2)

        # Điền mean cho các cột không lệch
        data[mean_cols] = data[mean_cols].fillna(data[mean_cols].mean()).round(2)
        
        # Chuyển các cột có kiểu dữ liệu số thành kiểu int nếu giá trị là số nguyên
        data[median_cols] = data[median_cols].applymap(lambda x: int(x) if x == int(x) else x)
        data[mean_cols] = data[mean_cols].applymap(lambda x: int(x) if x == int(x) else x)


    # Xử lý các cột chuỗi
    
    # Với các cột chỉ có 'Yes' và 'No' thì điền 'No'
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
            modes = data[other_cols].mode().iloc[0]  
            data[other_cols] = data[other_cols].fillna(modes)

    return data

def predict_depression_risk(data: pd.DataFrame) -> pd.Series:
    """
    Dự đoán mức độ trầm cảm của một người dựa trên các yếu tố có liên quan trong dữ liệu.
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

    # Tạo các mức độ rủi ro từ risk_scores
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

# Tạo cột "Depression Risk"
cleaned_data['Depression Risk'] = predict_depression_risk(cleaned_data)

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'dataset\\cleaned_and_predicted_data.csv'
cleaned_data.to_csv(output_path, index=False)



