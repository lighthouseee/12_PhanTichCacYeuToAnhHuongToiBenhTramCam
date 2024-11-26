import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
file_path = 'filtered_depression_data.csv'
data = pd.read_csv(file_path)

# Làm sạch và chuyển đổi dữ liệu
data['Age'] = data['Age'].astype(float, errors='ignore')  # Chuyển 'Age' thành float
data_cleaned = data.dropna(subset=['Age'])  # Loại bỏ các giá trị NaN

# Lọc dữ liệu theo nhóm nguy cơ 'High' và 'Very High'
valid_depression_risk = ['High', 'Very High']
filtered_data = data_cleaned[data_cleaned['Depression Risk'].isin(valid_depression_risk)]

# Thiết lập biểu đồ
plt.figure(figsize=(10, 6))

# Vẽ biểu đồ mật độ
colors = {'High': 'blue', 'Very High': 'red'}
for risk_level in valid_depression_risk:
    subset = filtered_data[filtered_data['Depression Risk'] == risk_level]
    density = subset['Age'].value_counts(normalize=True).sort_index()  # Tính mật độ
    plt.plot(
        density.index, density.values,
        label=risk_level,
        color=colors[risk_level],
        linewidth=1.5
    )

# Tùy chỉnh biểu đồ
plt.title('Age Distribution Density for High and Very High Depression Risk', fontsize=14, fontweight='bold')
plt.xlabel('Age (Tuổi)', fontsize=12)
plt.ylabel('Density (Mật độ)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()
plt.show()
