import os
from downloader.githubdownloader import GithubDownloader
from properties import GitHubAuthToken, dataFolderPath, gitExecutablePath
from downloader.gitdownloader import GitDownloader
from filemanager.dbmanager import DBManager

def download_repo(repo_address):
	repo_api_address = "https://api.github.com/repos/" + '/'.join(repo_address.split('/')[-2:])
	repo_name = '_'.join(repo_address.split('/')[-2:])

	ghd = GithubDownloader(GitHubAuthToken)
	gd = GitDownloader(gitExecutablePath)
	db = DBManager(os.path.join(dataFolderPath, repo_name))

	if not db.project_info_exists():
		project_info = ghd.download_object(repo_api_address)
		db.add_project_info(project_info)

	repo_issues_address = repo_api_address + "/issues"
	for issue in ghd.download_paginated_object(repo_issues_address, ["state=all"]):
		if not db.issue_exists(issue):
			issue = ghd.download_object(repo_issues_address + "/" + str(issue["number"]))
			db.add_project_issue(issue)

	repo_issue_comments_address = repo_issues_address + "/comments"
	for issue_comment in ghd.download_paginated_object(repo_issue_comments_address):
		if not db.issue_comment_exists(issue_comment):
			db.add_project_issue_comment(issue_comment)

	repo_issue_events_address = repo_issues_address + "/events"
	for issue_event in ghd.download_paginated_object(repo_issue_events_address):
		if not db.issue_event_exists(issue_event):
			db.add_project_issue_event(issue_event)

	repo_commits_address = repo_api_address + "/commits"
	for commit in ghd.download_paginated_object(repo_commits_address):
		if not db.commit_exists(commit):
			commit = ghd.download_object(repo_commits_address + "/" + str(commit["sha"]))
			db.add_project_commit(commit)

	repo_commit_comments_address = repo_api_address + "/comments"
	for commit_comment in ghd.download_paginated_object(repo_commit_comments_address):
		if not db.commit_comment_exists(commit_comment):
			db.add_project_commit_comment(commit_comment)

	git_repo_path = os.path.join(dataFolderPath, repo_name, "sourcecode")
	if not gd.git_repo_exists(git_repo_path):
		gd.git_clone(repo_address, git_repo_path)
	else:
		gd.git_pull(git_repo_path)

download_repo("https://github.com/user/repo")
