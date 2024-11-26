import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'filtered_depression_data.csv'
data = pd.read_csv(file_path)

# Prepare the data
education_vs_depression = data[['Education Level', 'Depression Risk']]

# Calculate counts grouped by 'Education Level' and 'Depression Risk'
education_depression_counts = education_vs_depression.value_counts().reset_index()
education_depression_counts.columns = ['Education Level', 'Depression Risk', 'Count']

# Sort the data by count in descending order
education_depression_sorted = education_depression_counts.sort_values(by='Count', ascending=False)

# Create a bar plot with data sorted in descending order
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
plt.show()
