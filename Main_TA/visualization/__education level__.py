import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu từ file CSV
file_path = 'filtered_depression_data.csv'
data = pd.read_csv(file_path)

# Chuẩn bị dữ liệu
education_vs_depression = data[['Education Level', 'Depression Risk']]

# Tính số lượng nhóm theo 'Education Level' và 'Depression Risk'
education_depression_counts = education_vs_depression.value_counts().reset_index()
education_depression_counts.columns = ['Education Level', 'Depression Risk', 'Count']

# Sắp xếp dữ liệu theo số lượng giảm dần
education_depression_sorted = education_depression_counts.sort_values(by='Count', ascending=False)

# Thiết lập biểu đồ
plt.figure(figsize=(12, 6))

# Áp dụng bảng màu gradient sáng từ Seaborn
sns.set(style="whitegrid")
palette = sns.color_palette("coolwarm", len(education_depression_sorted['Depression Risk'].unique()))

# Vẽ biểu đồ cột với dữ liệu được sắp xếp giảm dần
sns.barplot(
    data=education_depression_sorted, 
    x='Education Level', 
    y='Count', 
    hue='Depression Risk', 
    palette=palette,
    dodge=True
)

# Tùy chỉnh biểu đồ
plt.title('Rủi ro trầm cảm theo trình độ học vấn (Thứ tự giảm dần)', fontsize=14, fontweight='bold')
plt.xlabel('Trình độ học vấn', fontsize=12)
plt.ylabel('Số lượng', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Rủi ro trầm cảm', loc='upper right')
plt.tight_layout()
plt.show()
