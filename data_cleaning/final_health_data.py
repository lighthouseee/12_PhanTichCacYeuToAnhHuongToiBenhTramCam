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
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên trong khoảng từ 0 đến 120")
            elif col == 'Income':
                print(f"  Kiểu dữ liệu hợp lệ: Số nguyên hoặc số thực, giá trị không âm")
            elif col == 'Physical Activity Level':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Sedentary', 'Moderate', 'Active'")
            elif col == 'Smoking Status':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Current', 'Non-smoker', 'Former'")
            elif col == 'History of Mental Illness':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Yes', 'No'")
            elif col == 'Chronic Medical Conditions':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Yes', 'No'")
            elif col == 'Sleep Patterns':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Poor', 'Good', 'Fair'")
            elif col == 'Alcohol Consumption':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Low', 'Moderate', 'High'")
            elif col == 'Dietary Habits':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Healthy', 'Moderate', 'Unhealthy'")
            elif col == 'Employment Status':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Employed', 'Unemployed'")
            elif col == 'Family History of Depression':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Yes', 'No'")
            elif col == 'History of Substance Abuse':
                print(f"  Kiểu dữ liệu hợp lệ: Chuỗi với các giá trị có thể là: 'Yes', 'No'")
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
    
    # Kiểm tra mức độ hoạt động thể chất (Physical Activity Level)
    valid_physical_activity_levels = ['Sedentary', 'Moderate', 'Active']
    if not df['Physical Activity Level'].isin(valid_physical_activity_levels).all():
        issues['Physical Activity Level'] = "Mức độ hoạt động thể chất không hợp lệ."
    
    # Kiểm tra tình trạng hút thuốc (Smoking Status)
    valid_smoking_status = ['Non-smoker', 'Former', 'Current']
    if not df['Smoking Status'].isin(valid_smoking_status).all():
        issues['Smoking Status'] = "Tình trạng hút thuốc không hợp lệ."
    
    # Kiểm tra tình trạng việc làm (Employment Status)
    valid_employment_status = ['Employed', 'Unemployed']
    if not df['Employment Status'].isin(valid_employment_status).all():
        issues['Employment Status'] = "Tình trạng việc làm không hợp lệ."
    
    # Kiểm tra thói quen uống rượu bia (Alcohol Consumption)
    valid_alcohol_consumption = ['Low', 'Moderate', 'High']
    if not df['Alcohol Consumption'].isin(valid_alcohol_consumption).all():
        issues['Alcohol Consumption'] = "Thói quen uống rượu bia không hợp lệ."
    
    # Kiểm tra thói quen ăn uống (Dietary Habits)
    valid_dietary_habits = ['Healthy', 'Moderate', 'Unhealthy']
    if not df['Dietary Habits'].isin(valid_dietary_habits).all():
        issues['Dietary Habits'] = "Thói quen ăn uống không hợp lệ."
    
    # Kiểm tra thói quen ngủ (Sleep Patterns)
    valid_sleep_patterns = ['Poor', 'Good', 'Fair']
    if not df['Sleep Patterns'].isin(valid_sleep_patterns).all():
        issues['Sleep Patterns'] = "Thói quen ngủ không hợp lệ."
    
    # Kiểm tra tiền sử bệnh tâm lý (History of Mental Illness)
    valid_history_of_mental_illness = ['Yes', 'No']
    if not df['History of Mental Illness'].isin(valid_history_of_mental_illness).all():
        issues['History of Mental Illness'] = "Tiền sử bệnh tâm lý không hợp lệ."
    
    # Kiểm tra tiền sử lạm dụng chất kích thích (History of Substance Abuse)
    valid_history_of_substance_abuse = ['Yes', 'No']
    if not df['History of Substance Abuse'].isin(valid_history_of_substance_abuse).all():
        issues['History of Substance Abuse'] = "Tiền sử lạm dụng chất kích thích không hợp lệ."
    
    # Kiểm tra tiền sử gia đình bị trầm cảm (Family History of Depression)
    valid_family_history_of_depression = ['Yes', 'No']
    if not df['Family History of Depression'].isin(valid_family_history_of_depression).all():
        issues['Family History of Depression'] = "Tiền sử gia đình bị trầm cảm không hợp lệ."
    
    # Kiểm tra bệnh lý mãn tính (Chronic Medical Conditions)
    valid_chronic_medical_conditions = ['Yes', 'No']
    if not df['Chronic Medical Conditions'].isin(valid_chronic_medical_conditions).all():
        issues['Chronic Medical Conditions'] = "Bệnh lý mãn tính không hợp lệ."
    
    # Kiểm tra tình trạng hôn nhân (Marital Status)
    valid_marital_status = ['Single', 'Married', 'Divorced', 'Widowed']
    if not df['Marital Status'].isin(valid_marital_status).all():
        issues['Marital Status'] = "Tình trạng hôn nhân không hợp lệ."
    
    # Kiểm tra trình độ học vấn (Education Level)
    valid_education_level = ['High School', 'Bachelor\'s Degree', 'Master\'s Degree', 'Associate Degree', 'PhD']
    if not df['Education Level'].isin(valid_education_level).all():
        issues['Education Level'] = "Trình độ học vấn không hợp lệ."
    
    # Kiểm tra số lượng con cái (Number of Children)
    if (df['Number of Children'] < 0).any():
        issues['Number of Children'] = "Số lượng con cái không hợp lệ (số âm)."
    
    return issues

outliers = detect_outliers(data)
print("\nCác vấn đề bất thường:\n", outliers)

# 2. Kiểm tra dữ liệu thiếu (missing values)
missing_values = data.isnull().sum()
print("\nSố lượng giá trị thiếu trong từng cột:\n", missing_values)

# ----- Bước 2: Làm sạch dữ liệu -----

# 1. Loại bỏ giá trị bất thường
data = data[(data['Age'] >= 0) & (data['Age'] <= 120)]  # Tuổi trong khoảng 0-120
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

data = data[data['Number of Children'] >= 0]  # Không có số lượng con cái âm

# 3. Điền giá trị thiếu
for col in data.columns:
    if data[col].dtype in ['int64', 'float64']:
        data[col].fillna(data[col].mean())
    else:
        if col in ['History of Mental Illness', 'History of Substance Abuse',
                   'Family History of Depression', 'Chronic Medical Conditions']:
            data[col].fillna('No')
        else:
            data[col].fillna('Unknown')

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

# Kiểm tra kiểu dữ liệu của từng cột
print("Kiểu dữ liệu của từng cột trong dữ liệu sau khi thêm cột 'Depression Risk':\n")
print(data.dtypes)
# ----- Kết quả -----
# Thông tin sau khi làm sạch và thêm cột "Depression Risk"
print("\nDữ liệu sau khi làm sạch và thêm cột Depression Risk:\n")
print(data[['Age', 'Income', 'Physical Activity Level', 'Smoking Status', 'History of Mental Illness', 'Chronic Medical Conditions', 'Sleep Patterns', 'Depression Risk']].head())

# Lưu dữ liệu đã làm sạch vào file mới
output_path = 'cleaned_and_predicted_data.csv'

data.to_csv(output_path, index=False)
print(f"\nDữ liệu đã được lưu vào file '{output_path}'.")

# Đọc lại dữ liệu từ file mới
data_cleaned = pd.read_csv(output_path)

