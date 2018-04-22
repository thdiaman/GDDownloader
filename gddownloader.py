import os
import sys
import traceback
from logger.downloadlogger import Logger
from datamanager.dbmanager import DBManager
from downloader.gitdownloader import GitDownloader
from downloader.githubdownloader import GithubDownloader
from helpers import get_number_of, print_usage, read_file_in_lines
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath, verbose, \
	download_issues, download_issue_comments, download_issue_events, \
	download_commits, download_commit_comments, download_source_code, \
	download_issues_full, download_commits_full

# Initialize all required objects
db = DBManager()
lg = Logger(verbose)
ghd = GithubDownloader(GitHubAuthToken)
gd = GitDownloader(gitExecutablePath, lg)

def download_repo(repo_address):
	"""
	Downloads all the data of a repository given its GitHub URL.

	:param repo_address: the URL of the repository of which the data are downloaded.
	"""
	repo_api_address = "https://api.github.com/repos/" + '/'.join(repo_address.split('/')[-2:])
	repo_name = '_'.join(repo_address.split('/')[-2:])

	db.initialize_write_to_disk(repo_name)

	project = db.read_project_from_disk(repo_name)

	try:
		lg.log_action("Downloading project " + repo_name)
		if project.info_exists():
			lg.log_action("Project already exists! Updating...")
		project_info = ghd.download_object(repo_api_address)
		project.add_info(project_info)
		db.write_project_info_to_disk(repo_name, project["info"])
	
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
		project.add_stats(project_stats)
		lg.end_action()
		db.write_project_stats_to_disk(repo_name, project["stats"])
	
		if download_issues:
			lg.start_action("Retrieving issues...", project_stats["issues"])
			repo_issues_address = repo_api_address + "/issues"
			for issue in ghd.download_paginated_object(repo_issues_address, ["state=all"]):
				if not project.issue_exists(issue):
					if download_issues_full:
						issue = ghd.download_object(repo_issues_address + "/" + str(issue["number"]))
					project.add_issue(issue)
					db.write_project_issue_to_disk(repo_name, issue)
				lg.step_action()
			lg.end_action()
	
		if download_issue_comments:
			lg.start_action("Retrieving issue comments...", project_stats["issue_comments"])
			repo_issue_comments_address = repo_issues_address + "/comments"
			for issue_comment in ghd.download_paginated_object(repo_issue_comments_address):
				if not project.issue_comment_exists(issue_comment):
					project.add_issue_comment(issue_comment)
					db.write_project_issue_comment_to_disk(repo_name, issue_comment)
				lg.step_action()
			lg.end_action()
	
		if download_issue_events:
			lg.start_action("Retrieving issue events...", project_stats["issue_events"])
			repo_issue_events_address = repo_issues_address + "/events"
			for issue_event in ghd.download_paginated_object(repo_issue_events_address):
				if not project.issue_event_exists(issue_event):
					project.add_issue_event(issue_event)
					db.write_project_issue_event_to_disk(repo_name, issue_event)
				lg.step_action()
			lg.end_action()
	
		if download_commits:
			lg.start_action("Retrieving commits...", project_stats["commits"])
			repo_commits_address = repo_api_address + "/commits"
			for commit in ghd.download_paginated_object(repo_commits_address):
				if not project.commit_exists(commit):
					if download_commits_full:
						commit = ghd.download_object(repo_commits_address + "/" + str(commit["sha"]))
					project.add_commit(commit)
					db.write_project_commit_to_disk(repo_name, commit)
				lg.step_action()
			lg.end_action()
	
		if download_commit_comments:
			lg.start_action("Retrieving commit comments...", project_stats["commit_comments"])
			repo_commit_comments_address = repo_api_address + "/comments"
			for commit_comment in ghd.download_paginated_object(repo_commit_comments_address):
				if not project.commit_comment_exists(commit_comment):
					project.add_commit_comment(commit_comment)
					db.write_project_commit_comment_to_disk(repo_name, commit_comment)
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

	except Exception:
		# Catch any exception and print it before exiting
		sys.exit(traceback.format_exc())
	finally:
		# This line of code is always executed even if an exception occurs
		db.finalize_write_to_disk(repo_name, project)

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

