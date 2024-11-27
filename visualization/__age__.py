import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_age_distribution(data, save_path=None):
    """
    Vẽ biểu đồ mật độ phân phối tuổi theo nhóm nguy cơ.
    """
    plt.figure(figsize=(10, 6))
    colors = {'High': 'blue', 'Very High': 'red'}
    for risk_level in colors.keys():
        subset = data[data['Depression Risk'] == risk_level]
        density = subset['Age'].value_counts(normalize=True).sort_index()
        plt.plot(
            density.index, density.values,
            label=risk_level,
            color=colors[risk_level],
            linewidth=1.5
        )
    plt.title('Age Distribution Density', fontsize=14, fontweight='bold')
    plt.xlabel('Age')
    plt.ylabel('Density')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Biểu đồ đã được lưu tại: {save_path}")
    else:
        plt.show()

def plot_education_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ phân phối nguy cơ trầm cảm theo trình độ học vấn.
    """
    education_vs_depression = data[['Education Level', 'Depression Risk']]
    education_depression_counts = education_vs_depression.value_counts().reset_index()
    education_depression_counts.columns = ['Education Level', 'Depression Risk', 'Count']
    education_depression_sorted = education_depression_counts.sort_values(by='Count', ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=education_depression_sorted, 
        x='Education Level', 
        y='Count', 
        hue='Depression Risk', 
        palette='Set2',
        dodge=True
    )
    plt.title('Depression Risk by Education Level (Descending Order)', fontsize=14, fontweight='bold')
    plt.xlabel('Education Level', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Depression Risk', loc='upper right')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Biểu đồ đã được lưu tại: {save_path}")
    else:
        plt.show()

def plot_employment_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ phân phối nguy cơ trầm cảm theo trạng thái công việc với chú thích bên ngoài.
    """
    # Nhóm dữ liệu theo 'Employment Status' và 'Depression Risk'
    employment_depression = data.groupby(['Employment Status', 'Depression Risk']).size().unstack()

    # Chuẩn hóa thành phần trăm
    employment_depression_percentage = employment_depression.div(employment_depression.sum(axis=1), axis=0) * 100

    # Tạo biểu đồ pie chart
    num_pies = len(employment_depression_percentage.index)
    fig, axes = plt.subplots(1, num_pies, figsize=(6 * num_pies, 8))  # Tăng kích thước
    colors = sns.color_palette("pastel")
    wedges_props = {'edgecolor': 'black', 'linewidth': 1}

    for i, (employment_status, ax) in enumerate(zip(employment_depression_percentage.index, axes)):
        # Lấy dữ liệu của trạng thái công việc
        values = employment_depression_percentage.loc[employment_status]
        wedges, texts, autotexts = ax.pie(
            values,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops=wedges_props,
            labels=employment_depression_percentage.columns  # Thêm nhãn
        )
        ax.set_title(f'Employment: {employment_status}', fontsize=14, fontweight='bold')
        ax.set_ylabel('')  # Loại bỏ nhãn trục Y

    # Thêm chú thích bên ngoài
    fig.legend(
        labels=employment_depression_percentage.columns,
        loc='center right',  # Chú thích nằm bên phải biểu đồ
        title='Depression Risk',
        fontsize=12,
        title_fontsize=14,
        bbox_to_anchor=(1.2, 0.5)  # Điều chỉnh vị trí chú thích
    )

    # Tăng khoảng cách giữa các biểu đồ
    plt.subplots_adjust(wspace=0.5, right=0.85)  # Tăng khoảng cách giữa biểu đồ và chú thích

    # Hiển thị hoặc lưu biểu đồ
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Biểu đồ đã được lưu tại: {save_path}")
    else:
        plt.show()


# Chương trình chính
if __name__ == "__main__":
    # Đọc dữ liệu
    file_path_age_education = 'filtered_depression_data.csv'
    file_path_employment = 'cleaned_and_predicted_data.csv'
    data_age_education = pd.read_csv(file_path_age_education)
    data_employment = pd.read_csv(file_path_employment)

    # Vẽ từng biểu đồ
    print("Vẽ biểu đồ phân phối tuổi...")
    plot_age_distribution(data_age_education)
    # plot_age_distribution(data_age_education, save_path='age_distribution.png')

    print("Vẽ biểu đồ trình độ học vấn...")
    plot_education_vs_depression(data_age_education)
    # plot_education_vs_depression(data_age_education, save_path='education_vs_depression.png')

    print("Vẽ biểu đồ trạng thái công việc...")
    plot_employment_vs_depression(data_employment)
    # plot_employment_vs_depression(data_employment, save_path='employment_vs_depression.png')
