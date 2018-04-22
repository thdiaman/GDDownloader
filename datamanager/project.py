
class Project(dict):
	"""
	Class that includes the data of a GitHub project. This class is implemented as a dict
	and includes also several helper functions for adding data and checking for data.
	"""
	def info_exists(self):
		"""
		Checks if the info of the project exists.

		:returns: True if the project info exists, or False otherwise.
		"""
		return bool(self["info"])

	def add_info(self, info):
		"""
		Adds the info of the repository.

		:param info: the info to be added to the repository.
		"""
		self["info"] = info

	def stats_exists(self):
		"""
		Checks if the stats of the project exist.

		:returns: True if the project stats exist, or False otherwise.
		"""
		return bool(self["stats"])

	def add_stats(self, stats):
		"""
		Adds the stats of the repository.

		:param stats: the stats to be added to the repository.
		"""
		self["stats"] = stats

	def issue_exists(self, issue):
		"""
		Checks if the given issue exists in the project.

		:param issue: the issue to be checked.
		:returns: True if the given issue exists in the project, or False otherwise.
		"""
		return issue["id"] in self["issues"]

	def add_issue(self, issue):
		"""
		Adds an issue to the repository.

		:param issue: the issue to be added to the repository.
		"""
		self["issues"][issue["id"]] = issue

	def issue_comment_exists(self, issue_comment):
		"""
		Checks if the given issue comment exists in the project.

		:param issue_comment: the issue comment to be checked.
		:returns: True if the given issue comment exists in the project, or False otherwise.
		"""
		return issue_comment["id"] in self["issueComments"]

	def add_issue_comment(self, issue_comment):
		"""
		Adds an issue comment to the repository.

		:param issue_comment: the issue comment to be added to the repository.
		"""
		self["issueComments"][issue_comment["id"]] = issue_comment

	def issue_event_exists(self, issue_event):
		"""
		Checks if the given issue event exists in the project.

		:param issue_event: the issue event to be checked.
		:returns: True if the given issue event exists in the project, or False otherwise.
		"""
		return issue_event["id"] in self["issueEvents"]

	def add_issue_event(self, issue_event):
		"""
		Adds an issue event to the repository.

		:param issue_event: the issue event to be added to the repository.
		"""
		self["issueEvents"][issue_event["id"]] = issue_event

	def commit_exists(self, commit):
		"""
		Checks if the given commit exists in the project.

		:param commit: the commit to be checked.
		:returns: True if the given commit exists in the project, or False otherwise.
		"""
		return commit["sha"] in self["commits"]

	def add_commit(self, commit):
		"""
		Adds a commit to the repository.

		:param commit: the commit to be added to the repository.
		"""
		self["commits"][commit["sha"]] = commit

	def commit_comment_exists(self, commit_comment):
		"""
		Checks if the given commit comment exists in the project.

		:param commit_comment: the commit comment to be checked.
		:returns: True if the given commit comment exists in the project, or False otherwise.
		"""
		return commit_comment["id"] in self["commitComments"]

	def add_commit_comment(self, commit_comment):
		"""
		Adds a commit comment to the repository.

		:param commit_comment: the commit comment to be added to the repository.
		"""
		self["commitComments"][commit_comment["id"]] = commit_comment

