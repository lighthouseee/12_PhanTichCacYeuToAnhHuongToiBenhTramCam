import pandas as pd
import matplotlib.pyplot as plt

# Tải dữ liệu từ file
file_path = 'C:/Users/USER/Documents/GitHub/do_an_cuoi_ky_python/cleaned_and_predicted_data.csv'
data = pd.read_csv(file_path)

# Chuẩn bị dữ liệu để trực quan hóa
history_of_mental_illness = data['History of Mental Illness']
depression_risk = data['Depression Risk']

# Đếm số lượng của từng loại để vẽ biểu đồ cột xếp chồng
stacked_data = pd.crosstab(history_of_mental_illness, depression_risk)

# Tạo biểu đồ cột xếp chồng chi tiết và rõ ràng hơn
colors = ['#ff9999', '#66b3ff', '#99ff99']  # Bảng màu tùy chỉnh để hiển thị rõ ràng

# Vẽ biểu đồ cột xếp chồng
fig, ax = plt.subplots(figsize=(12, 7))
stacked_data.plot(kind='bar', stacked=True, color=colors, ax=ax, edgecolor='black')

# Tiêu đề và nhãn
ax.set_title('So sánh chi tiết giữa Tiền sử bệnh tâm thần và Nguy cơ trầm cảm', fontsize=16)
ax.set_xlabel('Tiền sử bệnh tâm thần', fontsize=14)
ax.set_ylabel('Số lượng cá nhân', fontsize=14)

# Thêm chú thích (legend) và chỉnh vị trí hiển thị
ax.legend(title='Nguy cơ trầm cảm', loc='upper right', fontsize=12, title_fontsize=12)

# Xoay nhãn trên trục x để dễ đọc hơn
plt.xticks(rotation=0, fontsize=12)

# Hiển thị lưới trên trục y để dễ so sánh
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Sắp xếp bố cục gọn gàng
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()
000