import pandas as pd
import matplotlib.pyplot as plt

# Load dữ liệu từ file CSV
file_path = 'cleaned_and_predicted_data.csv'
data = pd.read_csv(file_path)

# Nhóm dữ liệu theo 'Employment Status' và 'Depression Risk'
employment_depression = data.groupby(['Employment Status', 'Depression Risk']).size().unstack()

# Chuẩn hóa dữ liệu trong mỗi trạng thái công việc thành phần trăm
employment_depression_percentage = employment_depression.div(employment_depression.sum(axis=1), axis=0) * 100

# Tạo biểu đồ pie chart cho từng trạng thái công việc
fig, axes = plt.subplots(1, len(employment_depression_percentage), figsize=(15, 6))

for i, employment_status in enumerate(employment_depression_percentage.index):
    wedges, texts, autotexts = axes[i].pie(
        employment_depression_percentage.loc[employment_status],
        autopct='%1.1f%%',
        startangle=90
    )
    
    # Set the title for each subplot
    axes[i].set_title(f'Employment: {employment_status}')
    
    # Add legend outside the pie chart
    axes[i].legend(
        employment_depression_percentage.columns,
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    # Loại bỏ nhãn trục y để tăng thẩm mỹ
    axes[i].set_ylabel('')

# Căn chỉnh bố cục
plt.tight_layout()
plt.show()
