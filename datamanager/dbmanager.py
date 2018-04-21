import os
from properties import dataFolderPath
from datamanager.project import Project
from datamanager.filemanager import FileManager

class DBManager(FileManager):
	"""
	Class that implements a DB manager.
	"""
	def __init__(self):
		"""
		Initializes this DB manager.
		"""
		self.create_folder_if_it_does_not_exist(dataFolderPath)

	def create_directory_structure(self, repo_name):
		# Create all the necessary directories
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.create_folder_if_it_does_not_exist(rootfolder)
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issueComments"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issueEvents"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commits"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commitComments"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "sourcecode"))

	def read_project_from_disk(self, repo_name):
		# Read data from files
		project = Project()
		rootfolder = os.path.join(dataFolderPath, repo_name)
		project["info"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "info.json"))
		project["stats"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "stats.json"))
		project["issues"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues"), "id")
		project["issueComments"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issueComments"), "id")
		project["issueEvents"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issueEvents"), "id")
		project["commits"] = self.read_jsons_from_folder(os.path.join(rootfolder, "commits"), "sha")
		project["commitComments"] = self.read_jsons_from_folder(os.path.join(rootfolder, "commitComments"), "id")
		return project

	def write_project_to_disk(self, repo_name, project):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "info.json"), project["info"])
		self.write_json_to_file(os.path.join(rootfolder, "stats.json"), project["stats"])
		for issue in project["issues"].values():
			self.write_json_to_file(os.path.join(rootfolder, "issues", str(issue["id"]) + ".json"), issue)
		for issue_comment in project["issueComments"].values():
			self.write_json_to_file(os.path.join(rootfolder, "issueComments", str(issue_comment["id"]) + ".json"), issue_comment)
		for issue_event in project["issueEvents"].values():
			self.write_json_to_file(os.path.join(rootfolder, "issueEvents", str(issue_event["id"]) + ".json"), issue_event)
		for commit in project["commits"].values():
			self.write_json_to_file(os.path.join(rootfolder, "commits", str(commit["sha"]) + ".json"), commit)
		for commit_comment in project["commitComments"].values():
			self.write_json_to_file(os.path.join(rootfolder, "commitComments", str(commit_comment["id"]) + ".json"), commit_comment)

	def write_project_info_to_disk(self, repo_name, info):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "info.json"), info)

	def write_project_stats_to_disk(self, repo_name, stats):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "stats.json"), stats)

	def write_project_issue_to_disk(self, repo_name, issue):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "issues", str(issue["id"]) + ".json"), issue)

	def write_project_issue_comment_to_disk(self, repo_name, issue_comment):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "issueComments", str(issue_comment["id"]) + ".json"), issue_comment)

	def write_project_issue_event_to_disk(self, repo_name, issue_event):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "issueEvents", str(issue_event["id"]) + ".json"), issue_event)

	def write_project_commit_to_disk(self, repo_name, commit):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "commits", str(commit["sha"]) + ".json"), commit)

	def write_project_commit_comment_to_disk(self, repo_name, commit_comment):
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.write_json_to_file(os.path.join(rootfolder, "commitComments", str(commit_comment["id"]) + ".json"), commit_comment)

