import os
from filemanager.filemanager import FileManager

class DBManager(FileManager):
	"""
	Class that implements a DB manager.
	"""
	def __init__(self, rootfolder):
		"""
		Initializes this DB manager.
		
		:param rootfolder: folder where the data is stored.
		"""

		# Create all the necessary directories
		self.rootfolder = rootfolder
		if not os.path.exists(rootfolder):
			os.makedirs(rootfolder)
		if not os.path.exists(os.path.join(self.rootfolder, "issues")):
			os.makedirs(os.path.join(self.rootfolder, "issues"))
		if not os.path.exists(os.path.join(self.rootfolder, "issueComments")):
			os.makedirs(os.path.join(self.rootfolder, "issueComments"))
		if not os.path.exists(os.path.join(self.rootfolder, "issueEvents")):
			os.makedirs(os.path.join(self.rootfolder, "issueEvents"))
		if not os.path.exists(os.path.join(self.rootfolder, "commits")):
			os.makedirs(os.path.join(self.rootfolder, "commits"))
		if not os.path.exists(os.path.join(self.rootfolder, "commitComments")):
			os.makedirs(os.path.join(self.rootfolder, "commitComments"))
		if not os.path.exists(os.path.join(self.rootfolder, "sourcecode")):
			os.makedirs(os.path.join(self.rootfolder, "sourcecode"))

		self.project = {}
		if self.project_info_exists():
			self.project["info"] = self.read_json_from_file(os.path.join(self.rootfolder, "info.json"))

		self.project["stats"] = {}
		if self.project_stats_exists():
			self.project["stats"] = self.read_json_from_file(os.path.join(self.rootfolder, "stats.json"))

		self.project["issues"] = {}
		for issue_filename in os.listdir(os.path.join(self.rootfolder, "issues")):
			issue = self.read_json_from_file(os.path.join(self.rootfolder, "issues", issue_filename))
			self.project["issues"][issue["id"]] = issue

		self.project["issueComments"] = {}
		for issue_comment_filename in os.listdir(os.path.join(self.rootfolder, "issueComments")):
			issue_comment = self.read_json_from_file(os.path.join(self.rootfolder, "issueComments", issue_comment_filename))
			self.project["issueComments"][issue_comment["id"]] = issue_comment

		self.project["issueEvents"] = {}
		for issue_event_filename in os.listdir(os.path.join(self.rootfolder, "issueEvents")):
			issue_event = self.read_json_from_file(os.path.join(self.rootfolder, "issueEvents", issue_event_filename))
			self.project["issueEvents"][issue_event["id"]] = issue_event

		self.project["commits"] = {}
		for commit_filename in os.listdir(os.path.join(self.rootfolder, "commits")):
			commit = self.read_json_from_file(os.path.join(self.rootfolder, "commits", commit_filename))
			self.project["commits"][commit["sha"]] = commit

		self.project["commitComments"] = {}
		for commit_comment_filename in os.listdir(os.path.join(self.rootfolder, "commitComments")):
			commit_comment = self.read_json_from_file(os.path.join(self.rootfolder, "commitComments", commit_comment_filename))
			self.project["commitComments"][commit_comment["id"]] = commit_comment

	def project_info_exists(self):
		return os.path.exists(os.path.join(self.rootfolder, "info.json"))

	def add_project_info(self, info):
		self.project["info"] = info
		self.write_json_to_file(os.path.join(self.rootfolder, "info.json"), info)

	def project_stats_exists(self):
		return os.path.exists(os.path.join(self.rootfolder, "stats.json"))

	def add_project_stats(self, stats):
		self.project["stats"] = stats
		self.write_json_to_file(os.path.join(self.rootfolder, "stats.json"), stats)

	def issue_exists(self, issue):
		return issue["id"] in self.project["issues"]

	def add_project_issue(self, issue):
		self.project["issues"][issue["id"]] = issue
		self.write_json_to_file(os.path.join(self.rootfolder, "issues", str(issue["id"]) + ".json"), issue)

	def issue_comment_exists(self, issue_comment):
		return issue_comment["id"] in self.project["issueComments"]

	def add_project_issue_comment(self, issue_comment):
		self.project["issueComments"][issue_comment["id"]] = issue_comment
		self.write_json_to_file(os.path.join(self.rootfolder, "issueComments", str(issue_comment["id"]) + ".json"), issue_comment)

	def issue_event_exists(self, issue_event):
		return issue_event["id"] in self.project["issueEvents"]

	def add_project_issue_event(self, issue_event):
		self.project["issueEvents"][issue_event["id"]] = issue_event
		self.write_json_to_file(os.path.join(self.rootfolder, "issueEvents", str(issue_event["id"]) + ".json"), issue_event)

	def commit_exists(self, commit):
		return commit["sha"] in self.project["commits"]

	def add_project_commit(self, commit):
		self.project["commits"][commit["sha"]] = commit
		self.write_json_to_file(os.path.join(self.rootfolder, "commits", str(commit["sha"]) + ".json"), commit)

	def commit_comment_exists(self, commit_comment):
		return commit_comment["id"] in self.project["commitComments"]

	def add_project_commit_comment(self, commit_comment):
		self.project["commitComments"][commit_comment["id"]] = commit_comment
		self.write_json_to_file(os.path.join(self.rootfolder, "commitComments", str(commit_comment["id"]) + ".json"), commit_comment)
