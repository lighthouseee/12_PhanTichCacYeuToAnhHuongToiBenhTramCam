import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc file dữ liệu
file_path = 'cleaned_and_predicted_data.csv'
data = pd.read_csv(file_path)

# Tạo bảng pivot để so sánh giữa tình trạng hôn nhân và nguy cơ trầm cảm
heatmap_data = pd.crosstab(data['Marital Status'], data['Depression Risk'])

# Vẽ biểu đồ heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu', cbar=True)
plt.title('Comparison of Marital Status with Depression Risk')
plt.xlabel('Depression Risk')
plt.ylabel('Marital Status')
plt.tight_layout()
plt.show()
