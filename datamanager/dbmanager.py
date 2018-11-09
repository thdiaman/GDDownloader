import os
from datamanager.project import Project
from datamanager.filemanager import FileManager
from properties import dataFolderPath, always_write_to_disk

class DBManager(FileManager):
	"""
	Class that implements a DB manager. To use this class, you must first call the method
	initialize_write_to_disk, then optionally call any other method for writing data to
	disk, and finally call the method finalize_write_to_disk.
	"""
	def __init__(self):
		"""
		Initializes this DB manager.
		"""
		self.create_folder_if_it_does_not_exist(dataFolderPath)

	def initialize_write_to_disk(self, repo_name):
		"""
		Initializes the writing of a project to disk. Creates all the necessary directories.

		:param repo_name: the name of the repository to be written to disk.
		"""
		rootfolder = os.path.join(dataFolderPath, repo_name)
		self.create_folder_if_it_does_not_exist(rootfolder)
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issues"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issueComments"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "issueEvents"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commits"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "commitComments"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "contributors"))
		self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "sourcecode"))

	def read_project_from_disk(self, repo_name):
		"""
		Reads a project from disk given the name of the repository that is also the folder
		of the project.

		:param repo_name: the name of the repository to be read from disk.
		:returns: an object of type Project.
		"""
		project = Project()
		rootfolder = os.path.join(dataFolderPath, repo_name)
		project["info"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "info.json"))
		project["stats"] = self.read_json_from_file_if_it_exists(os.path.join(rootfolder, "stats.json"))
		project["issues"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issues"), "id")
		project["issueComments"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issueComments"), "id")
		project["issueEvents"] = self.read_jsons_from_folder(os.path.join(rootfolder, "issueEvents"), "id")
		project["commits"] = self.read_jsons_from_folder(os.path.join(rootfolder, "commits"), "sha")
		project["commitComments"] = self.read_jsons_from_folder(os.path.join(rootfolder, "commitComments"), "id")
		project["contributors"] = self.read_jsons_from_folder(os.path.join(rootfolder, "contributors"), "id")
		return project

	def project_exists(self, repo_name):
		"""
		Check if a project exists in the disk given the name of the repository that is also the folder
		of the project. The existence of the project is determined by whether it has an info.json file

		:param repo_name: the name of the repository to be read from disk.
		:returns: True if the project exists, or False otherwise.
		"""
		return os.path.exists(os.path.join(dataFolderPath, repo_name, "info.json"))

	def finalize_write_to_disk(self, repo_name, project):
		"""
		Finalizes the writing of a project to disk. Closes any open buffers.

		:param repo_name: the name of the repository to be written to disk.
		:param project: the repository data to be written to disk.
		"""
		if not always_write_to_disk:
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
			for contributor in project["contributors"].values():
				self.write_json_to_file(os.path.join(rootfolder, "contributors", str(contributor["id"]) + ".json"), contributor)

	def write_project_info_to_disk(self, repo_name, info):
		"""
		Writes the info of a repository to disk.

		:param repo_name: the name of the repository.
		:param info: the info to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "info.json"), info)

	def write_project_stats_to_disk(self, repo_name, stats):
		"""
		Writes the stats of a repository to disk.

		:param repo_name: the name of the repository.
		:param stats: the stats to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "stats.json"), stats)

	def write_project_issue_to_disk(self, repo_name, issue):
		"""
		Writes an issue of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue: the issue to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "issues", str(issue["id"]) + ".json"), issue)

	def write_project_issue_comment_to_disk(self, repo_name, issue_comment):
		"""
		Writes an issue comment of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue_comment: the issue comment to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "issueComments", str(issue_comment["id"]) + ".json"), issue_comment)

	def write_project_issue_event_to_disk(self, repo_name, issue_event):
		"""
		Writes an issue event of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue_event: the issue event to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "issueEvents", str(issue_event["id"]) + ".json"), issue_event)

	def write_project_commit_to_disk(self, repo_name, commit):
		"""
		Writes a commit of a repository to disk.

		:param repo_name: the name of the repository.
		:param commit: the commit to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "commits", str(commit["sha"]) + ".json"), commit)

	def write_project_commit_comment_to_disk(self, repo_name, commit_comment):
		"""
		Writes a commit comment of a repository to disk.

		:param repo_name: the name of the repository.
		:param commit_comment: the commit comment to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "commitComments", str(commit_comment["id"]) + ".json"), commit_comment)

	def write_project_contributor_to_disk(self, repo_name, contributor):
		"""
		Writes a contributor of a repository to disk.

		:param repo_name: the name of the repository.
		:param contributor: the contributor to be written to disk.
		"""
		if always_write_to_disk:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.write_json_to_file(os.path.join(rootfolder, "contributors", str(contributor["id"]) + ".json"), contributor)

