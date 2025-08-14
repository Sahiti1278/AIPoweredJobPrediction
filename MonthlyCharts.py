import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/sahitisriupputuri/Desktop/Singular /Predictive_TrainingData.csv")

# Convert all to lowercase
df['category_group'] = df['category_group'].str.lower()


df['category_group'] = df['category_group'].apply(normalize_role)

# Convert to datetime safely
df['posted_month_year'] = pd.to_datetime(df['posted_month_year'], errors='coerce')

# Drop rows where conversion failed
df = df.dropna(subset=['posted_month_year'])

# Normalize to month start
df['posted_month_year'] = df['posted_month_year'].dt.to_period('M').dt.to_timestamp()

# Keep only last 6 months
last_date = df['posted_month_year'].max()
cutoff_date = last_date - pd.DateOffset(months=5)
df = df[df['posted_month_year'] >= cutoff_date]

# Group by month & category
df_grouped = df.groupby(['posted_month_year', 'category_group'], as_index=False)['total_count'].sum()

# Plot each month separately, sorted descending
months = df_grouped['posted_month_year'].sort_values().unique()
for month in months:
    month_data = df_grouped[df_grouped['posted_month_year'] == month].sort_values(by='total_count', ascending=False)
    plt.figure(figsize=(12, 6))
    plt.bar(month_data['category_group'], month_data['total_count'], color='skyblue')
    plt.title(f'Job Postings - {month.strftime("%B %Y")}')
    plt.xlabel('Category')
    plt.ylabel('Total Postings')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
