import os
import sys
from filemanager.dbmanager import DBManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath

def download_repo(repo_address):
	repo_api_address = "https://api.github.com/repos/" + '/'.join(repo_address.split('/')[-2:])
	repo_name = '_'.join(repo_address.split('/')[-2:])

	print("Downloading project " + repo_name)
	ghd = GithubDownloader(GitHubAuthToken)
	gd = GitDownloader(gitExecutablePath)
	db = DBManager(os.path.join(dataFolderPath, repo_name))

	if db.project_info_exists():
		print("Project already exists! Updating...")
	else:
		project_info = ghd.download_object(repo_api_address)
		db.add_project_info(project_info)

	print("Downloading issues...", end=' ')
	repo_issues_address = repo_api_address + "/issues"
	for issue in ghd.download_paginated_object(repo_issues_address, ["state=all"]):
		if not db.issue_exists(issue):
			issue = ghd.download_object(repo_issues_address + "/" + str(issue["number"]))
			db.add_project_issue(issue)
	print("Done!")

	print("Downloading issue comments...", end=' ')
	repo_issue_comments_address = repo_issues_address + "/comments"
	for issue_comment in ghd.download_paginated_object(repo_issue_comments_address):
		if not db.issue_comment_exists(issue_comment):
			db.add_project_issue_comment(issue_comment)
	print("Done!")

	print("Downloading issue events...", end=' ')
	repo_issue_events_address = repo_issues_address + "/events"
	for issue_event in ghd.download_paginated_object(repo_issue_events_address):
		if not db.issue_event_exists(issue_event):
			db.add_project_issue_event(issue_event)
	print("Done!")

	print("Downloading commits...", end=' ')
	repo_commits_address = repo_api_address + "/commits"
	for commit in ghd.download_paginated_object(repo_commits_address):
		if not db.commit_exists(commit):
			commit = ghd.download_object(repo_commits_address + "/" + str(commit["sha"]))
			db.add_project_commit(commit)
	print("Done!")

	print("Downloading commit comments...", end=' ')
	repo_commit_comments_address = repo_api_address + "/comments"
	for commit_comment in ghd.download_paginated_object(repo_commit_comments_address):
		if not db.commit_comment_exists(commit_comment):
			db.add_project_commit_comment(commit_comment)
	print("Done!")

	print("Downloading source code...", end=' ')
	git_repo_path = os.path.join(dataFolderPath, repo_name, "sourcecode")
	if not gd.git_repo_exists(git_repo_path):
		gd.git_clone(repo_address, git_repo_path)
	else:
		gd.git_pull(git_repo_path)
	print("Done!")

def read_file_in_lines(filename):
	"""
	Reads a file into lines.
	
	:param filename: the filename of the file to be read.
	:returns: a list with the lines of the file.
	"""
	with open(filename) as infile:
		lines = infile.readlines()
	return lines

def print_usage():
	"""
	Prints the usage information of this python file.
	"""
	print("Usage: python main.py arg")
	print("where arg can be one of the following:")
	print("   github url (e.g. https://github.com/user/repo)")
	print("   path to txt file containing github urls")

if __name__ == "__main__":
	if ((not sys.argv) or len(sys.argv) <= 1):
		print_usage()
	elif(sys.argv[1].startswith("https://github.com")):
		download_repo(sys.argv[1])
	elif(os.path.exists(sys.argv[1])):
		repos = read_file_in_lines(sys.argv[1])
		for repo in repos:
			download_repo(sys.argv[1])
	else:
		print_usage()

