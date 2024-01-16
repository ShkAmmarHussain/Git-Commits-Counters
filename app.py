""" Create CSV of Commit Counts """
import csv
from commit_count import count_commits

REPO_URL = "Paste Link of Repo"

data = count_commits(REPO_URL)

# Specify the path for the CSV file
CSV_FILE_PATH = 'output.csv'

# Open the CSV file for writing
with open(CSV_FILE_PATH, 'w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the header
    csv_writer.writerow(['Branch', 'User', 'Commits'])

    # Write the data
    for branch, branch_data in data.items():
        commits = branch_data['commits']
        users_data = branch_data['users']

        for user, user_commits in users_data.items():
            csv_writer.writerow([branch, user, user_commits])

print(f"CSV file has been created: {CSV_FILE_PATH}")
