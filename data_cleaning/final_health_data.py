import pandas as pd
import numpy as np
from time import time

s_time = time()
# Đọc file CSV
file_path = 'depression_data.csv'  
data = pd.read_csv(file_path)

def detect_outliers(df: pd.DataFrame) -> dict:
    """
    Phát hiện giá trị bất thường trong dữ liệu.
    """
    num_conditions = {
        'Age': (df['Age'] < 18) | (df['Age'] > 80),
        'Income': df['Income'] < 0,
        'Number of Children': df['Number of Children'] < 0
    }

    cat_conditions = {
        'Physical Activity Level': ~df['Physical Activity Level'].isin(['Sedentary', 'Moderate', 'Active']),
        'Smoking Status': ~df['Smoking Status'].isin(['Non-smoker', 'Former', 'Current']),
        'Employment Status': ~df['Employment Status'].isin(['Employed', 'Unemployed']),
        'Alcohol Consumption': ~df['Alcohol Consumption'].isin(['Low', 'Moderate', 'High']),
        'Dietary Habits': ~df['Dietary Habits'].isin(['Healthy', 'Moderate', 'Unhealthy']),
        'Sleep Patterns': ~df['Sleep Patterns'].isin(['Poor', 'Good', 'Fair']),
        'History of Mental Illness': ~df['History of Mental Illness'].isin(['Yes', 'No']),
        'History of Substance Abuse': ~df['History of Substance Abuse'].isin(['Yes', 'No']),
        'Family History of Depression': ~df['Family History of Depression'].isin(['Yes', 'No']),
        'Chronic Medical Conditions': ~df['Chronic Medical Conditions'].isin(['Yes', 'No']),
        'Marital Status': ~df['Marital Status'].isin(['Single', 'Married', 'Divorced', 'Widowed']),
        'Education Level': ~df['Education Level'].isin(["High School", "Bachelor's Degree", "Master's Degree", "Associate Degree", "PhD"])
    }

    issues = {}
    for col, condition in {**num_conditions, **cat_conditions}.items():
        if condition.any():
            issues[col] = f"Cột {col} có giá trị bất thường."
    return issues

def remove_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Thay thế các giá trị bất thường bằng NaN trong DataFrame.
    """
    num_conditions = {
        'Age': (data['Age'] < 18) | (data['Age'] > 80),
        'Income': data['Income'] < 0,
        'Number of Children': data['Number of Children'] < 0
    }

    cat_conditions = {
        'Physical Activity Level': ~data['Physical Activity Level'].isin(['Sedentary', 'Moderate', 'Active']),
        'Smoking Status': ~data['Smoking Status'].isin(['Non-smoker', 'Former', 'Current']),
        'Employment Status': ~data['Employment Status'].isin(['Employed', 'Unemployed']),
        'Alcohol Consumption': ~data['Alcohol Consumption'].isin(['Low', 'Moderate', 'High']),
        'Dietary Habits': ~data['Dietary Habits'].isin(['Healthy', 'Moderate', 'Unhealthy']),
        'Sleep Patterns': ~data['Sleep Patterns'].isin(['Poor', 'Good', 'Fair']),
        'History of Mental Illness': ~data['History of Mental Illness'].isin(['Yes', 'No']),
        'Family History of Depression': ~data['Family History of Depression'].isin(['Yes', 'No']),
        'Chronic Medical Conditions': ~data['Chronic Medical Conditions'].isin(['Yes', 'No']),
        'Marital Status': ~data['Marital Status'].isin(['Single', 'Married', 'Divorced', 'Widowed']),
        'Education Level': ~data['Education Level'].isin(["High School", "Bachelor's Degree", "Master's Degree", "Associate Degree", "PhD"])
    }

    for column, condition in {**num_conditions, **cat_conditions}.items():
        data[column] = data[column].where(~condition, np.nan)

    return data

def fill_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Điền các giá trị thiếu trong DataFrame và làm tròn các giá trị số về số nguyên.
    """
    num_columns = data.select_dtypes(include=['int64', 'float64']).columns
    for col in num_columns:
        data[col] = data[col].fillna(data[col].mean())
        data[col] = data[col].round().astype(int)
    
    str_columns = data.select_dtypes(include=['object']).columns
    for col in str_columns:
        if col in ['History of Mental Illness', 'History of Substance Abuse', 'Family History of Depression', 'Chronic Medical Conditions']:
            data[col] = data[col].fillna('No')
        else:
            most_common_value = data[col].mode()[0]
            data[col] = data[col].fillna(most_common_value)

    return data

def predict_depression_risk_vectorized(data: pd.DataFrame) -> pd.Series:
    """
    Dự đoán mức độ trầm cảm dựa trên các yếu tố trong dữ liệu.
    """
    risk_scores = np.zeros(len(data))

    if (data['Income'] < 20000).any():
        risk_scores[data['Income'] < 20000] += 1
    
    if (data['Physical Activity Level'] == 'Sedentary').any():
        risk_scores[data['Physical Activity Level'] == 'Sedentary'] += 1
        
    if (data['Smoking Status'] == 'Current').any():
        risk_scores[data['Smoking Status'] == 'Current'] += 1

    if (data['History of Mental Illness'] == 'Yes').any():
        risk_scores[data['History of Mental Illness'] == 'Yes'] += 1
    
    if (data['Chronic Medical Conditions'] == 'Yes').any():
        risk_scores[data['Chronic Medical Conditions'] == 'Yes'] += 1
    
    if (data['Sleep Patterns'] == 'Poor').any():
        risk_scores[data['Sleep Patterns'] == 'Poor'] += 1
        
    if (data['Employment Status'] == 'Unemployed').any():
        risk_scores[data['Employment Status'] == 'Unemployed'] += 1

    if (data['Alcohol Consumption'] == 'High').any():
        risk_scores[data['Alcohol Consumption'] == 'High'] += 1

    if (data['Dietary Habits'] == 'Unhealthy').any():
        risk_scores[data['Dietary Habits'] == 'Unhealthy'] += 1

    if (data['History of Substance Abuse'] == 'Yes').any():
        risk_scores[data['History of Substance Abuse'] == 'Yes'] += 1

    if (data['Family History of Depression'] == 'Yes').any():
        risk_scores[data['Family History of Depression'] == 'Yes'] += 1

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
cleaned_data['Depression Risk'] = predict_depression_risk_vectorized(cleaned_data)

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'cleaned_and_predicted_data.csv'
cleaned_data.to_csv(output_path, index=False)

# Thời gian thực thi
e_time = time()
t = e_time - s_time
