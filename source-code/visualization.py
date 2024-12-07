import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Hàm hỗ trợ
def save_or_show_plot(save_path=None, verbose=True):
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
def plot_sleep_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ mối tương quan giữa Mẫu giấc ngủ và Nguy cơ trầm cảm.
    """
    sleep_vs_depression = data.groupby(['Sleep Patterns', 'Depression Risk']).size().unstack()
    sleep_vs_depression_reset = sleep_vs_depression.reset_index().melt(
        id_vars='Sleep Patterns', 
        var_name='Depression Risk', 
        value_name='Count'
    )

    plt.figure(figsize=(14, 8))
    barplot = sns.barplot(
        data=sleep_vs_depression_reset, 
        x='Sleep Patterns', 
        y='Count', 
        hue='Depression Risk', 
        palette="coolwarm"
    )

    plt.title('Sleep Patterns by Depression Risk', fontsize=16, pad=20)
    plt.xlabel('Sleep Patterns', fontsize=14, labelpad=10)
    plt.ylabel('Number of People', fontsize=14, labelpad=10)
    plt.legend(title='Depression Risk', fontsize=12)

    for p in barplot.patches:
        height = p.get_height()
        if height > 0:
            barplot.annotate(f'{int(height)}', 
                             (p.get_x() + p.get_width() / 2., height), 
                             ha='center', va='bottom', 
                             fontsize=10, color='black', 
                             xytext=(0, 3), textcoords='offset points')

    plt.tight_layout()
    save_or_show_plot(save_path)

def plot_marital_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ mối tương quan giữa Tình trạng hôn nhân và Nguy cơ trầm cảm.
    """
    marital_vs_depression = data.value_counts(['Marital Status', 'Depression Risk']).reset_index(name='Count')

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=marital_vs_depression, 
        x='Marital Status', 
        y='Count', 
        hue='Depression Risk', 
        palette='coolwarm'
    )

    plt.title('Marital status by Depression Risk', fontsize=16, pad=20)
    plt.xlabel('Tình trạng hôn nhân', fontsize=14)
    plt.ylabel('Số lượng người', fontsize=14)
    plt.legend(title='Nguy cơ trầm cảm', fontsize=12)

    for p in plt.gca().patches:
        plt.text(
            p.get_x() + p.get_width() / 2,  
            p.get_height(),                 
            f'{int(p.get_height())}',       
            ha='center', va='bottom',      
            fontsize=10, color='black'     
        )

    plt.tight_layout()
    save_or_show_plot(save_path)

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

def plot_education_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ phân phối nguy cơ trầm cảm theo trình độ học vấn.
    """
    education_vs_depression = data.value_counts(['Education Level', 'Depression Risk']).reset_index(name='Count')
    education_vs_depression = education_vs_depression.sort_values('Count', ascending=False)

    palette = sns.color_palette("hls", len(data['Depression Risk'].unique()))

    plt.figure(figsize=(12, 6))

    for risk, color in zip(data['Depression Risk'].unique(), palette):
        subset = education_vs_depression[education_vs_depression['Depression Risk'] == risk]
        bars = plt.bar(
            subset['Education Level'], subset['Count'], label=risk, alpha=0.7, color=color
        )

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
    save_or_show_plot(save_path)

def plot_employment_vs_depression(data, save_path=None):
    """
    Vẽ biểu đồ trạng thái việc làm theo nguy cơ trầm cảm.
    """
    depression_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
    data['Depression Risk'] = pd.Categorical(data['Depression Risk'], categories=depression_order, ordered=True)

    grouped_data = data.value_counts(['Depression Risk', 'Employment Status']).reset_index(name='Count')
    grouped_data = grouped_data.sort_values('Depression Risk')
    total_counts = grouped_data.groupby('Depression Risk')['Count'].transform('sum')
    grouped_data['Percentage'] = grouped_data['Count'] / total_counts * 100

    pivot_table = grouped_data.pivot(index='Depression Risk', columns='Employment Status', values='Percentage').fillna(0)

    pivot_table.plot(kind='bar', figsize=(12, 6), width=0.7, color=sns.color_palette("Set2", len(pivot_table.columns)))

    plt.title('Distribution of Employment Status by Depression Risk', fontsize=16, fontweight='bold')
    plt.xlabel('Depression Risk', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Employment Status', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    save_or_show_plot(save_path)

