import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

df = pd.read_csv("/Users/sahitisriupputuri/Desktop/Singular /Predictive_TrainingData.csv")

# Convert all to lowercase
df['category_group'] = df['category_group'].str.lower()

# Convert to datetime and filter last 6 months
df['posted_month_year'] = pd.to_datetime(df['posted_month_year'], errors='coerce')
df = df.dropna(subset=['posted_month_year'])
df['posted_month_year'] = df['posted_month_year'].dt.to_period('M').dt.to_timestamp()
last_date = df['posted_month_year'].max()
cutoff_date = last_date - pd.DateOffset(months=5)
df = df[df['posted_month_year'] >= cutoff_date]

# Group by month & category
df_grouped = df.groupby(['posted_month_year', 'category_group'], as_index=False)['total_count'].sum()

# Sort months
months = sorted(df_grouped['posted_month_year'].unique())

# Dashboard grid parameters
rows, cols = 2, 3
num_charts_per_fig = rows * cols
cmap = cm.get_cmap('tab20')  # multicolor bars

for i in range(0, len(months), num_charts_per_fig):
    current_months = months[i:i+num_charts_per_fig]
    fig, axes = plt.subplots(rows, cols, figsize=(20, 12))
    axes = axes.flatten()
    
    for ax, month in zip(axes, current_months):
        # Filter only this month
        month_data = df_grouped[df_grouped['posted_month_year'] == month]
    
        month_data = month_data[month_data['category_group'] != 'others']
        
        # Take top 20 for this month
        month_top20 = month_data.sort_values(by='total_count', ascending=False).head(20)
        
        colors = [cmap(j % 20) for j in range(len(month_top20))]
        bars = ax.barh(month_top20['category_group'], month_top20['total_count'], color=colors)
        ax.invert_yaxis()
        ax.set_title(f'Top 20 Jobs - {month.strftime("%B %Y")}')
        ax.set_xlabel('Total Postings')
        ax.set_ylabel('Category')
        
        # Add counts
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, f'{int(width)}', va='center', fontsize=9)
    
    # Hide unused subplots
    for j in range(len(current_months), len(axes)):
        fig.delaxes(axes[j])
    
    plt.tight_layout()
    plt.show()
