import requests
import json
import pandas as pd
import re

# Configurable variables
git_hub_user_name = "ev2900"
bearer_token = open("token.txt", "r").read()

# Read in historic data
metric_data_views = pd.read_csv ("Metric_Data/views.csv")
metric_data_unique_visits = pd.read_csv ("Metric_Data/unique_visits.csv")

# Get list of all repositories for GitHub user
get_repos = requests.get("https://api.github.com/users/" + git_hub_user_name + "/repos?per_page=250")

# Add a new row if a row for the repository does not already exists
for repo in get_repos.json():

	repo_name = repo["name"]

	if not (metric_data_views["Repository_Name"] == repo_name).any():		
		
		new_row_df = pd.DataFrame({"Repository_Name": [repo_name]})
		
		metric_data_views = pd.concat([metric_data_views, new_row_df]) 
		print("New repository (views): " + repo_name)

	if not (metric_data_unique_visits["Repository_Name"] == repo_name).any():
		
		new_row_df = pd.DataFrame({"Repository_Name": [repo_name]})
		
		metric_data_unique_visits = pd.concat([metric_data_unique_visits, new_row_df])
		print("New repository (unique visits): " + repo_name)

for repo in get_repos.json():

	# Get traffic (ie. page views, unique visitor) for each repository
	get_traffic = requests.get("https://api.github.com/repos/" + git_hub_user_name + "/" + repo["name"] + "/traffic/views", headers = {"Accept": "application/vnd.github+json", "Authorization" : "Bearer " + bearer_token, "X-GitHub-Api-Version" : "2022-11-28"})

	# Iterate over traffic data by date
	for date in get_traffic.json()["views"]:
		
		repo_name = repo["name"]
		timestamp = date["timestamp"]
		views = date["count"]
		unique_visits = date["uniques"]

		# Add view data to data frame
		metric_data_views.loc[metric_data_views.Repository_Name == repo_name,timestamp] = views
		print("Updating number of views for " + repo_name + " at " + str(timestamp))

		# Add unique vists to data frame
		metric_data_unique_visits.loc[metric_data_unique_visits.Repository_Name == repo_name,timestamp] = unique_visits
		print("Updating number of unique vists for " + repo_name + " at " + str(timestamp))


# Sort the columns in the views data frame by chronological order
metric_data_views = metric_data_views.reindex(sorted(metric_data_views.columns), axis=1)
metric_data_views = metric_data_views[ ['Repository_Name'] + [ col for col in metric_data_views.columns if col != 'Repository_Name' ] ]
metric_data_views.drop(metric_data_views.columns[len(metric_data_views.columns)-1], axis=1, inplace=True)

# Write the updated views data frame to CSV
metric_data_views.to_csv("Metric_Data/views.csv", index=False)

# Sort the columns in the unique views data frame by chronological order
metric_data_unique_visits = metric_data_unique_visits.reindex(sorted(metric_data_unique_visits.columns), axis=1)
metric_data_unique_visits = metric_data_unique_visits[ ['Repository_Name'] + [ col for col in metric_data_unique_visits.columns if col != 'Repository_Name' ] ]
metric_data_unique_visits.drop(metric_data_unique_visits.columns[len(metric_data_unique_visits.columns)-1], axis=1, inplace=True)

# Write the updated unique visits data frame to CSV
metric_data_unique_visits.to_csv("Metric_Data/unique_visits.csv", index=False)