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
		self.create_folder_if_it_does_not_exist(rootfolder)
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issueComments"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issueEvents"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commits"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commitComments"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "sourcecode"))

		# Read data from files
		self.project = {}
		self.project["info"] = self.read_json_from_file_if_it_exists(os.path.join(self.rootfolder, "info.json"))
		self.project["stats"] = self.read_json_from_file_if_it_exists(os.path.join(self.rootfolder, "stats.json"))
		self.project["issues"] = self.read_jsons_from_folder(os.path.join(self.rootfolder, "issues"), "id")
		self.project["issueComments"] = self.read_jsons_from_folder(os.path.join(self.rootfolder, "issueComments"), "id")
		self.project["issueEvents"] = self.read_jsons_from_folder(os.path.join(self.rootfolder, "issueEvents"), "id")
		self.project["commits"] = self.read_jsons_from_folder(os.path.join(self.rootfolder, "commits"), "sha")
		self.project["commitComments"] = self.read_jsons_from_folder(os.path.join(self.rootfolder, "commitComments"), "id")

	def project_info_exists(self):
		return bool(self.project["info"])

	def add_project_info(self, info):
		self.project["info"] = info
		self.write_json_to_file(os.path.join(self.rootfolder, "info.json"), info)

	def project_stats_exists(self):
		return bool(self.project["stats"])

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
