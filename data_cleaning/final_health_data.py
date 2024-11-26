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
    
    # Định nghĩa các điều kiện kiểm tra cho mỗi cột
    check_conditions = {
        'Age': lambda x: (x < 18) | (x > 80),
        'Income': lambda x: x < 0,
        'Number of Children': lambda x: x < 0,
        'Physical Activity Level': lambda x: ~x.isin(['Sedentary', 'Moderate', 'Active']),
        'Smoking Status': lambda x: ~x.isin(['Non-smoker', 'Former', 'Current']),
        'Employment Status': lambda x: ~x.isin(['Employed', 'Unemployed']),
        'Alcohol Consumption': lambda x: ~x.isin(['Low', 'Moderate', 'High']),
        'Dietary Habits': lambda x: ~x.isin(['Healthy', 'Moderate', 'Unhealthy']),
        'Sleep Patterns': lambda x: ~x.isin(['Poor', 'Good', 'Fair']),
        'History of Mental Illness': lambda x: ~x.isin(['Yes', 'No']),
        'History of Substance Abuse': lambda x: ~x.isin(['Yes', 'No']),
        'Family History of Depression': lambda x: ~x.isin(['Yes', 'No']),
        'Chronic Medical Conditions': lambda x: ~x.isin(['Yes', 'No']),
        'Marital Status': lambda x: ~x.isin(['Single', 'Married', 'Divorced', 'Widowed']),
        'Education Level': lambda x: ~x.isin(['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'Associate Degree', 'PhD'])
    }
    
    # Duyệt qua từng cột và kiểm tra điều kiện
    for col, condition in check_conditions.items():
        if condition(df[col]).any():
            issues[col] = f"{col} có giá trị bất thường."
    
    return issues

outliers = detect_outliers(data)
print("\nCác vấn đề bất thường:", outliers)

# 2. Kiểm tra dữ liệu thiếu (missing values)
missing_values = data.isnull().sum()
print("Số lượng giá trị thiếu trong từng cột:\n", missing_values)

# ----- Bước 2: Làm sạch dữ liệu -----

# 1. Loại bỏ giá trị bất thường
data = data[(data['Age'] >= 18) & (data['Age'] <= 80)]  # Tuổi trong khoảng 18-120
data = data[data['Income'] >= 0]  # Thu nhập không âm

valid_physical_activity_levels = ['Sedentary', 'Moderate', 'Active']
data = data[data['Physical Activity Level'].isin(valid_physical_activity_levels)]

valid_smoking_status = ['Non-smoker', 'Former', 'Current']
data = data[data['Smoking Status'].isin(valid_smoking_status)]

valid_employment_status = ['Employed', 'Unemployed']
data = data[data['Employment Status'].isin(valid_employment_status)]

valid_alcohol_consumption = ['Low', 'Moderate', 'High']
data = data[data['Alcohol Consumption'].isin(valid_alcohol_consumption)]

valid_dietary_habits = ['Healthy', 'Moderate', 'Unhealthy']
data = data[data['Dietary Habits'].isin(valid_dietary_habits)]

valid_sleep_patterns = ['Poor', 'Good', 'Fair']
data = data[data['Sleep Patterns'].isin(valid_sleep_patterns)]

valid_history_of_mental_illness = ['Yes', 'No']
data = data[data['History of Mental Illness'].isin(valid_history_of_mental_illness)]

valid_family_history_of_depression = ['Yes', 'No']
data = data[data['Family History of Depression'].isin(valid_family_history_of_depression)]

valid_chronic_medical_conditions = ['Yes', 'No']
data = data[data['Chronic Medical Conditions'].isin(valid_chronic_medical_conditions)]

valid_marital_status = ['Single', 'Married', 'Divorced', 'Widowed']
data = data[data['Marital Status'].isin(valid_marital_status)]

valid_education_level = ['High School', "Bachelor's Degree", "Master's Degree", 'Associate Degree', 'PhD']
data = data[data['Education Level'].isin(valid_education_level)]

data = data[data['Number of Children'] >= 0]  # Số lượng con cái không âm

# 3. Điền giá trị thiếu
for col in data.columns:
    if data[col].dtype in ['int64', 'float64']:  # Xử lý các cột số
        if col == 'Age':
            # Điền giá trị thiếu trong cột "Age" bằng giá trị trung bình của cột
            data[col].fillna(data[col].mean())
        elif col == 'Income':
            # Điền giá trị thiếu trong cột "Income" bằng giá trị trung bình của cột
            data[col].fillna(data[col].mean())
        elif col == 'Number of Children':
            # Điền giá trị thiếu trong cột "Number of Children"
            # Nếu tuổi < 18 thì điền 0, nếu tuổi >= 18 thì điền 1
            data[col] = data.apply(lambda row: 0 if row['Age'] < 18 else 1 if pd.isna(row[col]) else row[col], axis=1)
        else:
            # Điền giá trị thiếu cho các cột số khác (nếu có)
            data[col].fillna(data[col].mean())
    
    else:  # Xử lý các cột chuỗi
        if col in ['History of Mental Illness', 'History of Substance Abuse', 'Family History of Depression', 'Chronic Medical Conditions']:
            # Nếu là các cột này, điền 'No'
            data[col].fillna('No')
        else:
            # Còn lại điền ngẫu nhiên các giá trị khả dụng trong cột đó
            valid_values = data[col].dropna().unique()  # Lấy các giá trị không thiếu trong cột
            data[col] = data.apply(lambda row: np.random.choice(valid_values) if pd.isna(row[col]) else row[col], axis=1)

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
    # Lý do: Lối sống ít vận động đã được chứng minh là có liên quan đến nguy cơ trầm cảm cao hơn.
    # Hoạt động thể chất giúp giảm căng thẳng, cải thiện tâm trạng thông qua việc giải phóng endorphin.
    # Người ít vận động thường dễ bị cô lập xã hội, cảm giác mệt mỏi và các vấn đề sức khỏe khác (như béo phì, bệnh tim),
    # từ đó làm tăng nguy cơ trầm cảm.
    if row['Physical Activity Level'] == 'Sedentary':
        risk_score += 1
        
    # Hút thuốc (Smoking)
    # Lý do: Hút thuốc có liên hệ chặt chẽ với nguy cơ cao về sức khỏe tâm thần, bao gồm trầm cảm.
    # Nicotine có thể tạo cảm giác thoải mái tức thời, nhưng việc sử dụng lâu dài thường đi kèm với căng thẳng, lo âu,
    # và các rối loạn tâm thần. Ngoài ra, những người hút thuốc thường có xu hướng sử dụng thuốc lá như một cách đối phó
    # với áp lực, điều này có thể làm tình trạng tâm lý xấu đi theo thời gian.
    if row['Smoking Status'] == 'Current':
        risk_score += 1

    # Tiền sử bệnh tâm lý
    if row['History of Mental Illness'] == 'Yes':
        risk_score += 1
    
    # Bệnh lý mãn tính
    if row['Chronic Medical Conditions'] == 'Yes':
        risk_score += 1
    
    # Ngủ kém (Poor sleep quality)
    # Lý do: Giấc ngủ chất lượng kém hoặc thiếu ngủ có liên hệ trực tiếp với nguy cơ trầm cảm cao hơn.
    # Nó làm giảm khả năng điều chỉnh cảm xúc, gây mệt mỏi kéo dài và suy giảm hiệu suất trong cuộc sống.
    # Người bị rối loạn giấc ngủ thường dễ rơi vào vòng xoáy tiêu cực, từ đó làm tăng nguy cơ trầm cảm.
    if row['Sleep Patterns'] == 'Poor':
        risk_score += 1
        
    # Kiểm tra tình trạng thất nghiệp (Unemployed)
    # Lý do:
    # - Thất nghiệp là một yếu tố nguy cơ lớn cho trầm cảm do áp lực tài chính, cảm giác mất giá trị bản thân và cô lập xã hội.
    # - Nhiều nghiên cứu cho thấy người thất nghiệp có nguy cơ trầm cảm cao hơn, đặc biệt nếu tình trạng này kéo dài.
    if row['Employment Status'] == 'Unemployed':
        risk_score += 1

    # Thói quen uống rượu bia (Alcohol Consumption)
    # Lý do:
    # - Tiêu thụ rượu bia ở mức cao có thể gây ra những thay đổi trong hóa học não bộ và ảnh hưởng tiêu cực đến tâm trạng,
    #   dẫn đến nguy cơ cao mắc các vấn đề về sức khỏe tâm thần như trầm cảm và lo âu.
    # - Rượu bia cũng có thể làm giảm khả năng đối phó với căng thẳng, gia tăng các cảm giác tiêu cực và dẫn đến cô lập xã hội.
    # - Những người uống rượu bia quá mức có thể gặp khó khăn trong việc duy trì các mối quan hệ và công việc, do đó gia tăng nguy cơ trầm cảm.
    if row['Alcohol Consumption'] == 'High':
        risk_score += 1

    # Thói quen ăn uống không lành mạnh (Dietary Habits)
    # Lý do:
    # - Thói quen ăn uống không lành mạnh, đặc biệt là tiêu thụ nhiều thực phẩm chế biến sẵn, dầu mỡ và đường, có thể dẫn đến
    #   các vấn đề sức khỏe mãn tính như béo phì, bệnh tim mạch, và tiểu đường, những yếu tố có thể làm tăng nguy cơ trầm cảm.
    # - Chế độ ăn không đầy đủ chất dinh dưỡng có thể làm giảm mức độ serotonin trong não, gây ảnh hưởng tiêu cực đến tâm trạng
    #   và khả năng đối phó với căng thẳng.
    # - Những người có chế độ ăn không lành mạnh có thể cảm thấy mệt mỏi, thiếu năng lượng, và có ít động lực hơn trong cuộc sống,
    #   điều này làm tăng cảm giác thất bại và cô đơn, góp phần vào sự phát triển của trầm cảm.
    if row['Dietary Habits'] == 'Unhealthy':
        risk_score += 1

    # Tiền sử lạm dụng chất kích thích (History of Substance Abuse)
    # Lý do:
    # - Lạm dụng chất kích thích, bao gồm ma túy, thuốc lá, rượu bia, hoặc các chất khác, có thể làm thay đổi cấu trúc não bộ
    #   và gây ra sự mất cân bằng trong các chất dẫn truyền thần kinh, như serotonin và dopamine, góp phần làm gia tăng nguy cơ trầm cảm.
    # - Những người có tiền sử lạm dụng chất kích thích thường đối mặt với các vấn đề liên quan đến sức khỏe tâm thần, như lo âu,
    #   rối loạn cảm xúc và cảm giác trống rỗng, tất cả đều có thể dẫn đến trầm cảm.
    # - Lạm dụng chất kích thích còn có thể làm giảm khả năng xây dựng các mối quan hệ xã hội lành mạnh và duy trì công việc,
    #   dẫn đến cô lập, cảm giác vô giá trị và tăng khả năng mắc trầm cảm.
    if row['History of Substance Abuse'] == 'Yes':
        risk_score += 1

    # Tiền sử gia đình bị trầm cảm (Family History of Depression)
    # Lý do:
    # - Tiền sử gia đình bị trầm cảm là một yếu tố nguy cơ mạnh mẽ, vì các nghiên cứu đã chỉ ra rằng trầm cảm có thể di truyền.
    #   Những người có người thân trong gia đình mắc trầm cảm có nguy cơ cao hơn mắc phải tình trạng này do sự kết hợp giữa yếu tố di truyền và môi trường sống.
    # - Các gen liên quan đến cảm xúc, stress và các phản ứng sinh lý trong cơ thể có thể di truyền, làm tăng khả năng mắc trầm cảm.
    # - Bên cạnh yếu tố di truyền, những người có gia đình bị trầm cảm có thể dễ bị ảnh hưởng bởi các yếu tố môi trường như căng thẳng gia đình,
    #   thiếu hỗ trợ tâm lý và các trải nghiệm tiêu cực trong cuộc sống.
    if row['Family History of Depression'] == 'Yes':
        risk_score += 1

    # Phân loại mức độ trầm cảm dựa trên điểm số
    if risk_score >= 8:
        return 'Very High'
    elif risk_score >= 6:
        return 'High'
    elif risk_score >= 4:
        return 'Medium'
    elif risk_score >= 2:
        return 'Low'
    else:
        return 'Very Low'

# Áp dụng hàm dự đoán mức độ trầm cảm vào từng dòng dữ liệu
data['Depression Risk'] = data.apply(predict_depression_risk, axis=1)

# ----- Kết quả -----
# Thông tin sau khi làm sạch và thêm cột "Depression Risk"
print("\nDữ liệu sau khi làm sạch và thêm cột Depression Risk:\n")
print(data[['Name','Age', 'Income', 'Physical Activity Level', 'Smoking Status', 'History of Mental Illness', 'Chronic Medical Conditions', 'Sleep Patterns', 'Depression Risk']].head())

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'cleaned_and_predicted_data.csv'

data.to_csv(output_path, index=False)
print(f"\nDữ liệu đã được lưu vào file '{output_path}'.")


