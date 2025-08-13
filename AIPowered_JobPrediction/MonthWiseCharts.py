import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/sahitisriupputuri/Desktop/Singular /Predictive_TrainingData.csv")

# Step 1: Convert all to lowercase
df['category_group'] = df['category_group'].str.lower()

# Step 2: Merge similar categories
def normalize_role(role):
    if '.net' in role or 'dot net' in role or 'net' in role:
        return '.net developer'
    elif 'java' in role or 'developers' in role:
        return 'java developer'
    elif 'full' in role:
        return 'full stack developer'
    elif 'data engineer' in role:
        return 'data engineer'
    elif 'business' in role or 'business system' in role:
        return 'business analyst'
    elif 'devops' in role:
        return 'devops engineer'
    elif 'aws' in role:
        return 'aws engineer'
    elif 'cloud' in role:
        return 'cloud engineer'
    elif 'sap' in role:
        return 'sap hana/ead consultant'
    elif 'azure' in role:
        return 'azure data/devops engineer'
    elif 'software' in role:
        return 'software development engineer'
    elif 'python' in role:
        return 'python developer'
    elif 'qa' in role or 'quality' in role:
        return 'qa engineer'
    elif 'system engineer' in role:
        return 'system engineer'
    elif 'web' in role:
        return 'web developer'
    elif 'procurement' in role:
        return 'procurement specialist manager'
    elif 'sourcing' in role or 'staffing' in role or 'category' in role:
        return 'sourcing/staffing category manager'
    elif 'technical' in role:
        return 'technical lead'
    elif 'supply chain' in role:
        return 'supply chain manager'
    elif 'project manager' in role:
        return 'project manager'
    elif 'data analyst' in role or 'analytics' in role:
        return 'data analyst'
    elif 'angular' in role:
        return 'angular developer'
    elif 'front end' in role or 'front-end' in role or 'reactjs' in role or 'node' in role:
        return 'front end developer'
    elif 'ios' in role:
        return 'ios developer'
    elif 'oracle' in role:
        return 'oracle developer'
    elif 'architect' in role or 'etl' in role:
        return 'data solution architect'
    elif 'php' in role:
        return 'php developer'
    elif 'warehouse' in role:
        return 'warehouse supervisor/manager'
    elif 'snowflake' in role:
        return 'snowflake developer'
    elif 'salesforce' in role:
        return 'salesforce developer'
    elif 'logistics' in role:
        return 'logistics coordinator/manager'
    elif 'cyber' in role:
        return 'cyber security analyst'
    elif 'microsoft' in role:
        return 'microsoft services power apps developer'
    elif 'cobol' in role:
        return 'cobol developer'
    elif 'inventory' in role:
        return 'inventory control specialist'
    elif 'scientist' in role or 'science' in role:
        return 'data scientist'
    elif 'share' in role:
        return 'share point developer'
    elif 'sdet' in role or 'test' in role:
        return 'software test engineer'
    elif 'power' in role or 'bi' in role:
        return 'power bi developer'
    elif 'kinaxsis' in role:
        return 'kinaxsis integration'
    return role

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
