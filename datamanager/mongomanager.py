import os
import pymongo
from datamanager.project import Project
from datamanager.filemanager import FileManager
from datamanager.databasemanager import DatabaseManager
from properties import dataFolderPath, always_write_to_disk, database_host_and_port, \
	download_source_code

class MongoDBManager(DatabaseManager, FileManager):
	"""
	Class that implements a MongoDB manager. To use this class, you must first call the method
	initialize_write_to_disk, then optionally call any other method for writing data to
	disk, and finally call the method finalize_write_to_disk.
	"""
	def __init__(self):
		"""
		Initializes this DB manager.
		"""
		self.client = pymongo.MongoClient(database_host_and_port)
		self.db = self.client["alparet-github"]
		self.projects = self.db["projects"]
		self.stats = self.db["stats"]
		self.issues = self.db["issues"]
		self.issueComments = self.db["issueComments"]
		self.issueEvents = self.db["issueEvents"]
		self.commits = self.db["commits"]
		self.commitComments = self.db["commitComments"]
		self.contributors = self.db["contributors"]
		self.milestones = self.db["milestones"]
		self.releases = self.db["releases"]
		self.pulls = self.db["pulls"]
		self.pullComments = self.db["pullComments"]
		if download_source_code:
			self.create_folder_if_it_does_not_exist(dataFolderPath)  # this is required for downloading source code

	def initialize_write_to_disk(self, repo_name):
		"""
		Initializes the writing of a project to disk. In the case of MongoDB, it creates only a directory
		for downloading source code.

		:param repo_name: the name of the repository to be written to disk.
		"""
		if download_source_code:
			rootfolder = os.path.join(dataFolderPath, repo_name)
			self.create_folder_if_it_does_not_exist(rootfolder)
			self.create_folder_if_it_does_not_exist(os.path.join(rootfolder, "sourcecode"))

	def read_project_from_disk(self, repo_name):
		"""
		Reads a project from disk given the name of the repository.

		:param repo_name: the name of the repository to be read from disk.
		:returns: an object of type Project.
		"""
		project = Project()
		project["info"] = self.projects.find_one({"repo_name": repo_name})
		project["stats"] = self.stats.find_one({"repo_name": repo_name})
		project["issues"] = {obj["_id"]: obj for obj in self.issues.find({"repo_name": repo_name})}
		project["issueComments"] = {obj["_id"]: obj for obj in self.issueComments.find({"repo_name": repo_name})}
		project["issueEvents"] = {obj["_id"]: obj for obj in self.issueEvents.find({"repo_name": repo_name})}
		project["commits"] = {obj["_id"]: obj for obj in self.commits.find({"repo_name": repo_name})}
		project["commitComments"] = {obj["_id"]: obj for obj in self.commitComments.find({"repo_name": repo_name})}
		project["contributors"] = {obj["_id"]: obj for obj in self.contributors.find({"repo_name": repo_name})}
		project["milestones"] = {obj["_id"]: obj for obj in self.milestones.find({"repo_name": repo_name})}
		project["releases"] = {obj["_id"]: obj for obj in self.releases.find({"repo_name": repo_name})}
		project["pulls"] = {obj["_id"]: obj for obj in self.pulls.find({"repo_name": repo_name})}
		project["pullComments"] = {obj["_id"]: obj for obj in self.pullComments.find({"repo_name": repo_name})}
		return project

	def project_exists(self, repo_name):
		"""
		Check if a project exists in the disk given the name of the repository. The
		existence of the project is determined by whether it has an info.json file.

		:param repo_name: the name of the repository to be read from disk.
		:returns: True if the project exists, or False otherwise.
		"""
		return self.projects.find_one({"repo_name": repo_name})

	def project_crawl_complete(self, repo_name):
		"""
		Checks whether the last crawl of a project was completed normally. This is a lightweight check
		(it only reads the crawl flag, not the whole project). Projects that were downloaded before this
		flag was introduced are reported as not complete.

		:param repo_name: the name of the repository.
		:returns: True if the last crawl of the project was complete, or False otherwise.
		"""
		info = self.projects.find_one({"repo_name": repo_name}, {"lastcrawlcomplete": 1})
		return bool(info) and bool(info.get("lastcrawlcomplete", False))

	def finalize_write_to_disk(self, repo_name, project, crawldatetime, lastcrawlcomplete):
		"""
		Finalizes the writing of a project to disk. Closes any open buffers.

		:param repo_name: the name of the repository to be written to disk.
		:param project: the repository data to be written to disk.
		:param crawldatetime: the time that this crawl started.
		:param lastcrawlcomplete: the status of the last crawl, either True for complete of False otherwise.
		"""
		if not always_write_to_disk:
			project["info"]["_id"] = project["info"]["id"]
			project["info"]["repo_name"] = repo_name
			self.projects.update_one({"_id": project["info"]["_id"]}, {"$set": project["info"]}, upsert = True)
			project["stats"]["_id"] = project["info"]["id"]
			project["stats"]["repo_name"] = repo_name
			self.stats.update_one({"_id": project["stats"]["_id"]}, {"$set": project["stats"]}, upsert = True)
			for issue in project["issues"].values():
				issue["_id"] = issue["id"]
				issue["repo_name"] = repo_name
			self.update_multiple(self.issues, project["issues"].values(), upsert = True)
			for issue_comment in project["issueComments"].values():
				issue_comment["_id"] = issue_comment["id"]
				issue_comment["repo_name"] = repo_name
			self.update_multiple(self.issueComments, project["issueComments"].values(), upsert = True)
			for issue_event in project["issueEvents"].values():
				issue_event["_id"] = issue_event["id"]
				issue_event["repo_name"] = repo_name
			self.update_multiple(self.issueEvents, project["issueEvents"].values(), upsert = True)
			for commit in project["commits"].values():
				commit["_id"] = commit["sha"]
				commit["repo_name"] = repo_name
			self.update_multiple(self.commits, project["commits"].values(), upsert = True)
			for commit_comment in project["commitComments"].values():
				commit_comment["_id"] = commit_comment["id"]
				commit_comment["repo_name"] = repo_name
			self.update_multiple(self.commitComments, project["commitComments"].values(), upsert = True)
			for contributor in project["contributors"].values():
				contributor["_id"] = repo_name + "___" + str(contributor["id"])
				contributor["repo_name"] = repo_name
			self.update_multiple(self.contributors, project["contributors"].values(), upsert = True)
			for milestone in project["milestones"].values():
				milestone["_id"] = milestone["id"]
				milestone["repo_name"] = repo_name
			self.update_multiple(self.milestones, project["milestones"].values(), upsert = True)
			for release in project["releases"].values():
				release["_id"] = release["id"]
				release["repo_name"] = repo_name
			self.update_multiple(self.releases, project["releases"].values(), upsert = True)
			for pull in project["pulls"].values():
				pull["_id"] = pull["id"]
				pull["repo_name"] = repo_name
			self.update_multiple(self.pulls, project["pulls"].values(), upsert = True)
			for pull_comment in project["pullComments"].values():
				pull_comment["_id"] = pull_comment["id"]
				pull_comment["repo_name"] = repo_name
			self.update_multiple(self.pullComments, project["pullComments"].values(), upsert = True)
		if project.info_exists() and "_id" in project["info"]:
			# Record the outcome of this crawl (only the two crawl-status fields are touched)
			self.projects.update_one({"_id": project["info"]["_id"]}, {"$set": {"lastcrawlcomplete": lastcrawlcomplete, "lastcrawled": crawldatetime}}, upsert = True)

	def write_project_info_to_disk(self, repo_name, info):
		"""
		Writes the info of a repository to disk.

		:param repo_name: the name of the repository.
		:param info: the info to be written to disk.
		"""
		if always_write_to_disk:
			info["_id"] = info["id"]
			info["repo_name"] = repo_name
			self.projects.update_one({"_id": info["_id"]}, {"$set": info}, upsert = True)

	def write_project_stats_to_disk(self, repo_name, info, stats):
		"""
		Writes the stats of a repository to disk.

		:param repo_name: the name of the repository.
		:param info: the info of the project.
		:param stats: the stats to be written to disk.
		"""
		if always_write_to_disk:
			stats["_id"] = info["id"]
			stats["repo_name"] = repo_name
			self.stats.update_one({"_id": stats["_id"]}, {"$set": stats}, upsert = True)

	def write_project_issue_to_disk(self, repo_name, issue):
		"""
		Writes an issue of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue: the issue to be written to disk.
		"""
		if always_write_to_disk:
			issue["_id"] = issue["id"]
			issue["repo_name"] = repo_name
			self.issues.update_one({"_id": issue["_id"]}, {"$set": issue}, upsert = True)

	def write_project_issue_comment_to_disk(self, repo_name, issue_comment):
		"""
		Writes an issue comment of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue_comment: the issue comment to be written to disk.
		"""
		if always_write_to_disk:
			issue_comment["_id"] = issue_comment["id"]
			issue_comment["repo_name"] = repo_name
			self.issueComments.update_one({"_id": issue_comment["_id"]}, {"$set": issue_comment}, upsert = True)

	def write_project_issue_event_to_disk(self, repo_name, issue_event):
		"""
		Writes an issue event of a repository to disk.

		:param repo_name: the name of the repository.
		:param issue_event: the issue event to be written to disk.
		"""
		if always_write_to_disk:
			issue_event["_id"] = issue_event["id"]
			issue_event["repo_name"] = repo_name
			self.issueEvents.update_one({"_id": issue_event["_id"]}, {"$set": issue_event}, upsert = True)

	def write_project_commit_to_disk(self, repo_name, commit):
		"""
		Writes a commit of a repository to disk.

		:param repo_name: the name of the repository.
		:param commit: the commit to be written to disk.
		"""
		if always_write_to_disk:
			commit["_id"] = commit["sha"]
			commit["repo_name"] = repo_name
			self.commits.update_one({"_id": commit["_id"]}, {"$set": commit}, upsert = True)

	def write_project_commit_comment_to_disk(self, repo_name, commit_comment):
		"""
		Writes a commit comment of a repository to disk.

		:param repo_name: the name of the repository.
		:param commit_comment: the commit comment to be written to disk.
		"""
		if always_write_to_disk:
			commit_comment["_id"] = commit_comment["id"]
			commit_comment["repo_name"] = repo_name
			self.commitComments.update_one({"_id": commit_comment["_id"]}, {"$set": commit_comment}, upsert = True)

	def write_project_contributor_to_disk(self, repo_name, contributor):
		"""
		Writes a contributor of a repository to disk.

		:param repo_name: the name of the repository.
		:param contributor: the contributor to be written to disk.
		"""
		if always_write_to_disk:
			contributor["_id"] = repo_name + "___" + str(contributor["id"])
			contributor["repo_name"] = repo_name
			self.contributors.update_one({"_id": contributor["_id"]}, {"$set": contributor}, upsert = True)

	def write_project_milestone_to_disk(self, repo_name, milestone):
		"""
		Writes a milestone of a repository to disk.

		:param repo_name: the name of the repository.
		:param milestone: the milestone to be written to disk.
		"""
		if always_write_to_disk:
			milestone["_id"] = milestone["id"]
			milestone["repo_name"] = repo_name
			self.milestones.update_one({"_id": milestone["_id"]}, {"$set": milestone}, upsert = True)

	def write_project_release_to_disk(self, repo_name, release):
		"""
		Writes a release of a repository to disk.

		:param repo_name: the name of the repository.
		:param release: the release to be written to disk.
		"""
		if always_write_to_disk:
			release["_id"] = release["id"]
			release["repo_name"] = repo_name
			self.releases.update_one({"_id": release["_id"]}, {"$set": release}, upsert = True)

	def write_project_pull_to_disk(self, repo_name, pull):
		"""
		Writes a pull request of a repository to disk.

		:param repo_name: the name of the repository.
		:param pull: the pull request to be written to disk.
		"""
		if always_write_to_disk:
			pull["_id"] = pull["id"]
			pull["repo_name"] = repo_name
			self.pulls.update_one({"_id": pull["_id"]}, {"$set": pull}, upsert = True)

	def write_project_pull_comment_to_disk(self, repo_name, pull_comment):
		"""
		Writes a pull request comment of a repository to disk.

		:param repo_name: the name of the repository.
		:param pull_comment: the pull request comment to be written to disk.
		"""
		if always_write_to_disk:
			pull_comment["_id"] = pull_comment["id"]
			pull_comment["repo_name"] = repo_name
			self.pullComments.update_one({"_id": pull_comment["_id"]}, {"$set": pull_comment}, upsert = True)
