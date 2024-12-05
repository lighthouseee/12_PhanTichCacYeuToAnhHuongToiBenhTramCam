import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Hàm hỗ trợ
def save_or_show_plot(save_path, verbose=True):
    """
    Lưu hoặc hiển thị biểu đồ.
    """
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        if verbose:
            print(f"Biểu đồ đã được lưu tại: {save_path}")
    else:
        plt.show()

# Các hàm vẽ biểu đồ
def plot_age_distribution(data, save_path=None, colors=None):
    """
    Vẽ biểu đồ mật độ phân phối tuổi theo nhóm nguy cơ.
    """
    plt.figure(figsize=(10, 6))
    if colors is None:
        colors = {'High': 'blue', 'Very High': 'red'}
    
    for risk_level, color in colors.items():
        subset = data[data['Depression Risk'] == risk_level]
        density = subset.groupby('Age').size() / len(subset)
        plt.plot(
            density.index, density.values,
            label=risk_level, color=color, linewidth=1.5
        )
    plt.title('Density of Age Groups by Depression Risk', fontsize=14, fontweight='bold')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    save_or_show_plot(save_path)

import seaborn as sns

def plot_education_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ phân phối nguy cơ trầm cảm theo trình độ học vấn.
    """
    education_vs_depression = data.value_counts(['Education Level', 'Depression Risk']).reset_index(name='Count')
    education_vs_depression = education_vs_depression.sort_values('Count', ascending=False)

    # Tạo bảng màu đẹp hơn
    palette = sns.color_palette("hls", len(data['Depression Risk'].unique()))

    plt.figure(figsize=(12, 6))

    # Vẽ biểu đồ cột với màu sắc
    for risk, color in zip(data['Depression Risk'].unique(), palette):
        subset = education_vs_depression[education_vs_depression['Depression Risk'] == risk]
        bars = plt.bar(
            subset['Education Level'], subset['Count'], label=risk, alpha=0.7, color=color
        )

        # Hiển thị số liệu trên các cột
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2, height,
                f'{int(height)}', ha='center', va='bottom', fontsize=10
            )

    plt.title('Distribution of Depression Risk by Education Level', fontsize=14, fontweight='bold')
    plt.xlabel('Education Level', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Depression Risk', loc='upper right')
    plt.tight_layout()
    
    # Lưu hoặc hiển thị biểu đồ
    save_or_show_plot(save_path)
    
def plot_employment_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ cột đôi thể hiện tỷ lệ trạng thái việc làm theo nguy cơ trầm cảm.
    """
    # Sắp xếp thứ tự Depression Risk
    depression_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    data['Depression Risk'] = pd.Categorical(data['Depression Risk'], categories=depression_order, ordered=True)

    # Tính số lượng và tỷ lệ phần trăm
    grouped_data = data.value_counts(['Depression Risk', 'Employment Status']).reset_index(name='Count')
    grouped_data = grouped_data.sort_values('Depression Risk')
    total_counts = grouped_data.groupby('Depression Risk', observed=False)['Count'].transform('sum')  # Sửa lỗi
    grouped_data['Percentage'] = grouped_data['Count'] / total_counts * 100

    # Pivot để chuyển đổi dữ liệu cho biểu đồ cột đôi
    pivot_table = grouped_data.pivot(index='Depression Risk', columns='Employment Status', values='Percentage').fillna(0)

    # Vẽ biểu đồ cột đôi
    pivot_table.plot(kind='bar', figsize=(12, 6), width=0.7, color=sns.color_palette("Set2", len(pivot_table.columns)))

    # Thêm tiêu đề và nhãn
    plt.title('Distribution of Employment Status by Depression Risk', fontsize=16, fontweight='bold')
    plt.xlabel('Depression Risk', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Employment Status', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    save_or_show_plot(save_path)

# Chương trình chính
if __name__ == "__main__":
    # Đọc dữ liệu
    file_path_age_education = 'dataset\\filtered_depression_data.csv'
    file_path_employment = 'dataset\\cleaned_and_predicted_data.csv'
    data_age_education = pd.read_csv(file_path_age_education)
    data_employment = pd.read_csv(file_path_employment)

    # Vẽ từng biểu đồ
    plot_age_distribution(data_age_education)
    # plot_age_distribution(data_age_education, save_path='age_distribution.png')

    plot_education_vs_depression(data_age_education)
    # plot_education_vs_depression(data_age_education, save_path='education_vs_depression.png')

    plot_employment_vs_depression(data_employment)
    # plot_employment_vs_depression(data_employment, save_path='employment_vs_depression.png')
