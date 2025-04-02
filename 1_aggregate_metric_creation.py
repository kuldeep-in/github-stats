import pandas as pd

# Read in raw data
views = pd.read_csv('Metric_Data/views.csv')
unique_visits = pd.read_csv('Metric_Data/unique_visits.csv')

# VIEWS - summing all columns except the first column by row
views['Total'] = views.iloc[:, 1:].sum(axis=1).astype(int)

views = views.sort_values(by='Total', ascending=False)

views[['Repository_Name', 'Total']].to_csv("Aggregated_Metric_Data/agg_views.csv", index=False)

# UNIQUE VISTS - summing all columns except the first column by row
unique_visits['Total'] = unique_visits.iloc[:, 1:].sum(axis=1).astype(int)

unique_visits = unique_visits.sort_values(by='Total', ascending=False)

unique_visits[['Repository_Name', 'Total']].to_csv("Aggregated_Metric_Data/agg_unique_visits.csv", index=False)