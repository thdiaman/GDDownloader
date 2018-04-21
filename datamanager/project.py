
class Project(dict):
	def project_info_exists(self):
		return bool(self["info"])

	def add_project_info(self, info):
		self["info"] = info

	def project_stats_exists(self):
		return bool(self["stats"])

	def add_project_stats(self, stats):
		self["stats"] = stats

	def issue_exists(self, issue):
		return issue["id"] in self["issues"]

	def add_project_issue(self, issue):
		self["issues"][issue["id"]] = issue

	def issue_comment_exists(self, issue_comment):
		return issue_comment["id"] in self["issueComments"]

	def add_project_issue_comment(self, issue_comment):
		self["issueComments"][issue_comment["id"]] = issue_comment

	def issue_event_exists(self, issue_event):
		return issue_event["id"] in self["issueEvents"]

	def add_project_issue_event(self, issue_event):
		self["issueEvents"][issue_event["id"]] = issue_event

	def commit_exists(self, commit):
		return commit["sha"] in self["commits"]

	def add_project_commit(self, commit):
		self["commits"][commit["sha"]] = commit

	def commit_comment_exists(self, commit_comment):
		return commit_comment["id"] in self["commitComments"]

	def add_project_commit_comment(self, commit_comment):
		self["commitComments"][commit_comment["id"]] = commit_comment

