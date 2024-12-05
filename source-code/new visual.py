import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path_1 = 'dataset\\filtered_depression_data.csv'
file_path_2 = 'dataset\\cleaned_and_predicted_data.csv'



# Đọc dữ liệu từ hai file CSV
data_1 = pd.read_csv(file_path_1)
data_2 = pd.read_csv(file_path_2)

# Biểu đồ 1: Mối tương quan giữa Mẫu giấc ngủ và Nguy cơ trầm cảm
sleep_vs_depression = data_1.groupby(['Sleep Patterns', 'Depression Risk']).size().unstack()
sleep_vs_depression_reset = sleep_vs_depression.reset_index().melt(id_vars='Sleep Patterns', 
                                                                   var_name='Depression Risk', 
                                                                   value_name='Count')

plt.figure(figsize=(14, 8))
barplot = sns.barplot(data=sleep_vs_depression_reset, 
                      x='Sleep Patterns', 
                      y='Count', 
                      hue='Depression Risk', 
                      palette="coolwarm")  # Chọn palette 'coolwarm' (từ xanh lạnh đến đỏ nóng)

plt.title('Sleep Patterns by Depression Risk', fontsize=16, pad=20)
plt.xlabel('Sleep Patterns', fontsize=14, labelpad=10)
plt.ylabel('Number of People', fontsize=14, labelpad=10)
plt.legend(title='Depression Risk', fontsize=12)

for p in barplot.patches:
    height = p.get_height()
    if height > 0:  # Chỉ chú thích những cột có giá trị lớn hơn 0
        barplot.annotate(f'{int(height)}', 
                         (p.get_x() + p.get_width() / 2., height), 
                         ha='center', va='bottom', 
                         fontsize=10, color='black', 
                         xytext=(0, 3), textcoords='offset points')

plt.tight_layout()

# Biểu đồ 2: Mối tương quan giữa Tình trạng hôn nhân và Nguy cơ trầm cảm
marital_vs_depression = data_2.value_counts(['Marital Status', 'Depression Risk']).reset_index(name='Count')

plt.figure(figsize=(12, 6))

# Vẽ biểu đồ với palette 'coolwarm' để tạo màu sắc chuyển từ xanh lạnh đến đỏ nóng
sns.barplot(data=marital_vs_depression, x='Marital Status', y='Count', hue='Depression Risk', palette='coolwarm')  

plt.title('Mối tương quan giữa Tình trạng hôn nhân và Nguy cơ trầm cảm', fontsize=16)
plt.xlabel('Tình trạng hôn nhân', fontsize=14)
plt.ylabel('Số lượng người', fontsize=14)
plt.legend(title='Nguy cơ trầm cảm', fontsize=12)

# Thêm chú thích số lượng trên mỗi cột
for p in plt.gca().patches:
    plt.text(
        p.get_x() + p.get_width() / 2,  
        p.get_height(),                 
        f'{int(p.get_height())}',       
        ha='center', va='bottom',      
        fontsize=10, color='black'     
    )

plt.tight_layout()

# Hiển thị cả hai biểu đồ
plt.show()
0000