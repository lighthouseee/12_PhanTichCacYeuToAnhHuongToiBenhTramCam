import pandas as pd
import numpy as np
from time import time

s_time = time()
# Đọc file CSV
file_path = 'depression_data.csv'  
data = pd.read_csv(file_path)

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
            print(f"  Các giá trị hợp lệ có thể bao gồm: {unique_values[:10]} ...")  
        elif df[col].dtype in ['int64', 'float64']:
            # Các cột kiểu số
            if col == 'Age':
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên trong khoảng từ 18 đến 80")
            elif col == 'Income':
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên hoặc số thực không âm")
            else: # Số lượng con cái
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên không âm")
        else:
            print(f"  Không xác định được kiểu dữ liệu hợp lệ.")
        
def check_outlier_conditions(df: pd.DataFrame, col_conditions: dict) -> dict:
    """
    Hàm chung để kiểm tra các điều kiện bất thường (outlier) cho các cột.
    
    Args:
        df (pd.DataFrame): DataFrame cần kiểm tra.
        col_conditions (dict): Từ điển chứa tên cột và điều kiện kiểm tra bất thường.
        
    Returns:
        dict: Từ điển chứa các cột có giá trị bất thường.
    """
    issues = {}
    for col, condition in col_conditions.items():
        if condition.any():
            issues[col] = f"Cột {col} có giá trị bất thường."
    return issues

def detect_outliers(df: pd.DataFrame) -> dict:
    """
    Phát hiện giá trị bất thường trong dữ liệu bằng cách áp dụng vector hóa.
    
    Args:
        df (pd.DataFrame): Dữ liệu cần kiểm tra.
    
    Returns:
        dict: Từ điển chứa các cột có giá trị bất thường và mô tả vấn đề.
    """
    # Điều kiện cho các cột số
    num_conditions = {
        'Age': (df['Age'] < 18) | (df['Age'] > 80),
        'Income': df['Income'] < 0,
        'Number of Children': df['Number of Children'] < 0
    }

    # Điều kiện cho các cột phân loại
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
    issues.update(check_outlier_conditions(df, num_conditions))  # Kiểm tra các cột số
    issues.update(check_outlier_conditions(df, cat_conditions))  # Kiểm tra các cột phân loại

    return issues

def remove_outliers(data: pd.DataFrame) -> pd.DataFrame:
    """
    Thay thế các giá trị bất thường bằng NaN trong DataFrame dựa trên các điều kiện hợp lệ.
    
    Args:
        data (pd.DataFrame): DataFrame cần xử lý.
    
    Returns:
        pd.DataFrame: DataFrame đã thay thế giá trị bất thường bằng NaN.
    """
    # Điều kiện cho các cột số
    num_conditions = {
        'Age': (data['Age'] < 18) | (data['Age'] > 80),
        'Income': data['Income'] < 0,
        'Number of Children': data['Number of Children'] < 0
    }

    # Điều kiện cho các cột phân loại
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

    # Áp dụng các điều kiện để thay thế giá trị không hợp lệ bằng NaN
    for column, condition in {**num_conditions, **cat_conditions}.items():
        data[column] = data[column].where(~condition, np.nan)

    return data

def fill_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Điền các giá trị thiếu trong DataFrame và làm tròn các giá trị số về số nguyên.
    
    Args:
        data (pd.DataFrame): DataFrame cần điền giá trị thiếu và làm tròn các giá trị số.
        
    Returns:
        pd.DataFrame: DataFrame đã được điền giá trị thiếu và làm tròn các giá trị số.
    """
    # Xử lý các cột số
    num_columns = data.select_dtypes(include=['int64', 'float64']).columns
    for col in num_columns:
        # Điền giá trị thiếu bằng giá trị trung bình cho các cột số
        data[col] = data[col].fillna(data[col].mean())
        # Làm tròn các giá trị số thành số nguyên
        data[col] = data[col].round().astype(int)
    
    # Xử lý các cột chuỗi
    str_columns = data.select_dtypes(include=['object']).columns
    for col in str_columns:
        if col in ['History of Mental Illness', 'History of Substance Abuse', 'Family History of Depression', 'Chronic Medical Conditions']:
            data[col] = data[col].fillna('No')  # Điền 'No' cho các cột này
        else:
            most_common_value = data[col].mode()[0]
            data[col] = data[col].fillna(most_common_value)  # Điền giá trị phổ biến cho các cột chuỗi

    return data

def predict_depression_risk_vectorized(data: pd.DataFrame) -> pd.Series:
    """
    Dự đoán mức độ trầm cảm dựa trên các yếu tố trong dữ liệu.

    Args:
        data (pd.DataFrame): Dữ liệu đầu vào.

    Returns:
        pd.Series: Mức độ trầm cảm của từng dòng trong dữ liệu.
    """
    risk_scores = np.zeros(len(data))  # Khởi tạo mảng điểm số rủi ro

    # Thu nhập thấp (dưới 20,000)
    if (data['Income'] < 20000).any():
        risk_scores[data['Income'] < 20000] += 1
    
    # Tình trạng hoạt động thể chất ít (Sedentary)
    # Lý do: Lối sống ít vận động đã được chứng minh là có liên quan đến nguy cơ trầm cảm cao hơn.
    # Hoạt động thể chất giúp giảm căng thẳng, cải thiện tâm trạng thông qua việc giải phóng endorphin.
    # Người ít vận động thường dễ bị cô lập xã hội, cảm giác mệt mỏi và các vấn đề sức khỏe khác (như béo phì, bệnh tim),
    # từ đó làm tăng nguy cơ trầm cảm.
    if (data['Physical Activity Level'] == 'Sedentary').any():
        risk_scores[data['Physical Activity Level'] == 'Sedentary'] += 1
        
    # Hút thuốc (Smoking)
    # Lý do: Hút thuốc có liên hệ chặt chẽ với nguy cơ cao về sức khỏe tâm thần, bao gồm trầm cảm.
    # Nicotine có thể tạo cảm giác thoải mái tức thời, nhưng việc sử dụng lâu dài thường đi kèm với căng thẳng, lo âu,
    # và các rối loạn tâm thần. Ngoài ra, những người hút thuốc thường có xu hướng sử dụng thuốc lá như một cách đối phó
    # với áp lực, điều này có thể làm tình trạng tâm lý xấu đi theo thời gian.
    if (data['Smoking Status'] == 'Current').any():
        risk_scores[data['Smoking Status'] == 'Current'] += 1

    # Tiền sử bệnh tâm lý
    if (data['History of Mental Illness'] == 'Yes').any():
        risk_scores[data['History of Mental Illness'] == 'Yes'] += 1
    
    # Bệnh lý mãn tính
    if (data['Chronic Medical Conditions'] == 'Yes').any():
        risk_scores[data['Chronic Medical Conditions'] == 'Yes'] += 1
    
    # Ngủ kém (Poor sleep quality)
    # Lý do: Giấc ngủ chất lượng kém hoặc thiếu ngủ có liên hệ trực tiếp với nguy cơ trầm cảm cao hơn.
    # Nó làm giảm khả năng điều chỉnh cảm xúc, gây mệt mỏi kéo dài và suy giảm hiệu suất trong cuộc sống.
    # Người bị rối loạn giấc ngủ thường dễ rơi vào vòng xoáy tiêu cực, từ đó làm tăng nguy cơ trầm cảm.
    if (data['Sleep Patterns'] == 'Poor').any():
        risk_scores[data['Sleep Patterns'] == 'Poor'] += 1
        
    # Kiểm tra tình trạng thất nghiệp (Unemployed)
    # Lý do:
    # - Thất nghiệp là một yếu tố nguy cơ lớn cho trầm cảm do áp lực tài chính, cảm giác mất giá trị bản thân và cô lập xã hội.
    # - Nhiều nghiên cứu cho thấy người thất nghiệp có nguy cơ trầm cảm cao hơn, đặc biệt nếu tình trạng này kéo dài.
    if (data['Employment Status'] == 'Unemployed').any():
        risk_scores[data['Employment Status'] == 'Unemployed'] += 1

    # Thói quen uống rượu bia (Alcohol Consumption)
    # Lý do:
    # - Tiêu thụ rượu bia ở mức cao có thể gây ra những thay đổi trong hóa học não bộ và ảnh hưởng tiêu cực đến tâm trạng,
    #   dẫn đến nguy cơ cao mắc các vấn đề về sức khỏe tâm thần như trầm cảm và lo âu.
    # - Rượu bia cũng có thể làm giảm khả năng đối phó với căng thẳng, gia tăng các cảm giác tiêu cực và dẫn đến cô lập xã hội.
    # - Những người uống rượu bia quá mức có thể gặp khó khăn trong việc duy trì các mối quan hệ và công việc, do đó gia tăng nguy cơ trầm cảm.
    if (data['Alcohol Consumption'] == 'High').any():
        risk_scores[data['Alcohol Consumption'] == 'High'] += 1

    # Thói quen ăn uống không lành mạnh (Dietary Habits)
    # Lý do:
    # - Thói quen ăn uống không lành mạnh, đặc biệt là tiêu thụ nhiều thực phẩm chế biến sẵn, dầu mỡ và đường, có thể dẫn đến
    #   các vấn đề sức khỏe mãn tính như béo phì, bệnh tim mạch, và tiểu đường, những yếu tố có thể làm tăng nguy cơ trầm cảm.
    # - Chế độ ăn không đầy đủ chất dinh dưỡng có thể làm giảm mức độ serotonin trong não, gây ảnh hưởng tiêu cực đến tâm trạng
    #   và khả năng đối phó với căng thẳng.
    # - Những người có chế độ ăn không lành mạnh có thể cảm thấy mệt mỏi, thiếu năng lượng, và có ít động lực hơn trong cuộc sống,
    #   điều này làm tăng cảm giác thất bại và cô đơn, góp phần vào sự phát triển của trầm cảm.
    if (data['Dietary Habits'] == 'Unhealthy').any():
        risk_scores[data['Dietary Habits'] == 'Unhealthy'] += 1

    # Tiền sử lạm dụng chất kích thích (History of Substance Abuse)
    # Lý do:
    # - Lạm dụng chất kích thích, bao gồm ma túy, thuốc lá, rượu bia, hoặc các chất khác, có thể làm thay đổi cấu trúc não bộ
    #   và gây ra sự mất cân bằng trong các chất dẫn truyền thần kinh, như serotonin và dopamine, góp phần làm gia tăng nguy cơ trầm cảm.
    # - Những người có tiền sử lạm dụng chất kích thích thường đối mặt với các vấn đề liên quan đến sức khỏe tâm thần, như lo âu,
    #   rối loạn cảm xúc và cảm giác trống rỗng, tất cả đều có thể dẫn đến trầm cảm.
    # - Lạm dụng chất kích thích còn có thể làm giảm khả năng xây dựng các mối quan hệ xã hội lành mạnh và duy trì công việc,
    #   dẫn đến cô lập, cảm giác vô giá trị và tăng khả năng mắc trầm cảm.
    if (data['History of Substance Abuse'] == 'Yes').any():
        risk_scores[data['History of Substance Abuse'] == 'Yes'] += 1

    # Tiền sử gia đình bị trầm cảm (Family History of Depression)
    # Lý do:
    # - Tiền sử gia đình bị trầm cảm là một yếu tố nguy cơ mạnh mẽ, vì các nghiên cứu đã chỉ ra rằng trầm cảm có thể di truyền.
    #   Những người có người thân trong gia đình mắc trầm cảm có nguy cơ cao hơn mắc phải tình trạng này do sự kết hợp giữa yếu tố di truyền và môi trường sống.
    # - Các gen liên quan đến cảm xúc, stress và các phản ứng sinh lý trong cơ thể có thể di truyền, làm tăng khả năng mắc trầm cảm.
    # - Bên cạnh yếu tố di truyền, những người có gia đình bị trầm cảm có thể dễ bị ảnh hưởng bởi các yếu tố môi trường như căng thẳng gia đình,
    #   thiếu hỗ trợ tâm lý và các trải nghiệm tiêu cực trong cuộc sống.
    if (data['Family History of Depression'] == 'Yes').any():
        risk_scores[data['Family History of Depression'] == 'Yes'] += 1

    # Phân loại mức độ trầm cảm dựa trên điểm số
    depression_risk = pd.Series(np.select(
        [risk_scores >= 8, risk_scores >= 6, risk_scores >= 4, risk_scores >= 2], 
        ['Very High', 'High', 'Medium', 'Low'], 
        default='Very Low'
    ))

    return depression_risk

# ----- Kết quả -----

# Hiển thị thông tin tổng quan ban đầu
print("Một vài dòng dữ liệu:\n", data.head())

# ----- Mô tả các giá trị hợp lệ cho từng trường dữ liệu -----
describe_valid_values(data)

# ----- Bước 1: Phân tích dữ liệu -----
# 1. Kiểm tra giá trị bất thường
outliers = detect_outliers(data)
print("\nCác vấn đề bất thường:", outliers)

# 2. Kiểm tra dữ liệu thiếu (missing values)
missing_values = data.isnull().sum()
print("Số lượng giá trị thiếu trong từng cột:\n", missing_values)

# ----- Bước 2: Làm sạch dữ liệu -----
# 1. Loại bỏ giá trị bất thường
cleaned_data = remove_outliers(data)

# 2. Điền các giá trị thiếu
cleaned_data = fill_missing_values(cleaned_data)

# ----- Bước 3: Phát sinh dữ liệu mới -----
# Tạo cột "Depression Risk" - Đây là cột dự đoán xem một người có khả năng dẫn đến trầm cảm hay không dựa trên các điều kiện khách quan
# Áp dụng hàm dự đoán mức độ trầm cảm cho toàn bộ dữ liệu (dùng vectorized function thay vì apply từng dòng)
data['Depression Risk'] = predict_depression_risk_vectorized(data)

# Thông tin sau khi làm sạch và thêm cột "Depression Risk"
print("\nDữ liệu sau khi làm sạch và thêm cột Depression Risk:\n")
print(data[['Name','Age', 'Income', 'Physical Activity Level', 'Smoking Status', 'History of Mental Illness', 
            'Chronic Medical Conditions', 'Sleep Patterns', 'Depression Risk']].head())

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'cleaned_and_predicted_data.csv'
data.to_csv(output_path, index=False)
print(f"\nDữ liệu đã được lưu vào file '{output_path}'.")
e_time = time()
t = e_time - s_time
print(f"Thời gian thực thi {t:.2f} giây")


