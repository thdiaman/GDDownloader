# Set this to your GitHub auth token
GitHubAuthToken = 'add_here_your_token'

# Set this to the path of the git executable
gitExecutablePath = 'git'

# Set this to true to download also private repos if the token has private repo rights
include_private_repos = False

# Set this to False to skip existing repos
update_existing_repos = True

# Set to 0 for no messages, 1 for simple messages, and 2 for progress bars
verbose = 1

# Select how to write to disk (or how to send queries to the database)
always_write_to_disk = True

# Change these settings to store data in disk/database
use_database = 'disk' # (available options: disk, mongo)
# Disk settings
dataFolderPath = 'data' # Set this to the folder where data are downloaded
# Database settings
database_host_and_port = "mongodb://localhost:27017/"  # change this to the hostname and port of your database
num_bulk_operations = 1000 # set the number of operations that are sent as a bulk to the database

# Select what to download
download_issues = True
download_issue_comments = True
download_issue_events = True
download_commits = True
download_commit_comments = True
download_contributors = True
download_source_code = False

# Select whether the downloaded issues and commits information will be full
download_issues_full = True
download_commits_full = True
