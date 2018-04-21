import os
import sys
import json
from datamanager.dbmanager import DBManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose,\
	download_issues, download_issue_comments, download_issue_events,\
	download_commits, download_commit_comments, download_source_code
from logger.downloadlogger import Logger

def get_number_of(gdownloader, repo_api_address, statistic_type, param = None):
	r = gdownloader.download_request(repo_api_address + "/" + statistic_type, ["per_page=100"] if param == None else ["per_page=100", param])
	if "link" in r.headers:
		address = r.headers["link"].split(',')[1].split('<')[1].split('>')[0]
		data = gdownloader.download_object(address)
		return 100 * (int(address.split('=')[-1]) - 1) + len(data)
	else:
		data = json.loads(r.text or r.content)
		return len(data)

def download_repo(repo_address):
	repo_api_address = "https://api.github.com/repos/" + '/'.join(repo_address.split('/')[-2:])
	repo_name = '_'.join(repo_address.split('/')[-2:])

	ghd = GithubDownloader(GitHubAuthToken)
	gd = GitDownloader(gitExecutablePath)
	db = DBManager(os.path.join(dataFolderPath, repo_name))
	lg = Logger(verbose)

	lg.log_action("Downloading project " + repo_name)
	if db.project_info_exists():
		lg.log_action("Project already exists! Updating...")
	project_info = ghd.download_object(repo_api_address)
	db.add_project_info(project_info)

	lg.start_action("Retrieving project statistics...", 5)
	project_stats = {}
	project_stats["issues"] = get_number_of(ghd, repo_api_address, "issues", "state=all")
	lg.step_action()
	project_stats["issue_comments"] = get_number_of(ghd, repo_api_address, "issues/comments")
	lg.step_action()
	project_stats["issue_events"] = get_number_of(ghd, repo_api_address, "issues/events")
	lg.step_action()
	project_stats["commits"] = get_number_of(ghd, repo_api_address, "commits")
	lg.step_action()
	project_stats["commit_comments"] = get_number_of(ghd, repo_api_address, "comments")
	lg.step_action()
	db.add_project_stats(project_stats)
	lg.end_action()

	if download_issues:
		lg.start_action("Retrieving issues...", project_stats["issues"])
		repo_issues_address = repo_api_address + "/issues"
		for issue in ghd.download_paginated_object(repo_issues_address, ["state=all"]):
			if not db.issue_exists(issue):
				issue = ghd.download_object(repo_issues_address + "/" + str(issue["number"]))
				db.add_project_issue(issue)
			lg.step_action()
		lg.end_action()

	if download_issue_comments:
		lg.start_action("Retrieving issue comments...", project_stats["issue_comments"])
		repo_issue_comments_address = repo_issues_address + "/comments"
		for issue_comment in ghd.download_paginated_object(repo_issue_comments_address):
			if not db.issue_comment_exists(issue_comment):
				db.add_project_issue_comment(issue_comment)
			lg.step_action()
		lg.end_action()

	if download_issue_events:
		lg.start_action("Retrieving issue events...", project_stats["issue_events"])
		repo_issue_events_address = repo_issues_address + "/events"
		for issue_event in ghd.download_paginated_object(repo_issue_events_address):
			if not db.issue_event_exists(issue_event):
				db.add_project_issue_event(issue_event)
			lg.step_action()
		lg.end_action()

	if download_commits:
		lg.start_action("Retrieving commits...", project_stats["commits"])
		repo_commits_address = repo_api_address + "/commits"
		for commit in ghd.download_paginated_object(repo_commits_address):
			if not db.commit_exists(commit):
				commit = ghd.download_object(repo_commits_address + "/" + str(commit["sha"]))
				db.add_project_commit(commit)
			lg.step_action()
		lg.end_action()

	if download_commit_comments:
		lg.start_action("Retrieving commit comments...", project_stats["commit_comments"])
		repo_commit_comments_address = repo_api_address + "/comments"
		for commit_comment in ghd.download_paginated_object(repo_commit_comments_address):
			if not db.commit_comment_exists(commit_comment):
				db.add_project_commit_comment(commit_comment)
			lg.step_action()
		lg.end_action()

	if download_source_code:
		lg.start_action("Retrieving source code...")
		git_repo_path = os.path.join(dataFolderPath, repo_name, "sourcecode")
		if not gd.git_repo_exists(git_repo_path):
			gd.git_clone(repo_address, git_repo_path)
		else:
			gd.git_pull(git_repo_path)
		lg.end_action()

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

