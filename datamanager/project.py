
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

	def full_issue_exists(self, issue):
		"""
		Checks if the given issue exists in the project in its full version (including closed_by).

		:param issue: the issue to be checked.
		:returns: True if the given issue exists in the project, or False otherwise.
		"""
		if issue["id"] in self["issues"]:
			return "closed_by" in self["issues"][issue["id"]]
		else:
			return False

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

	def full_commit_exists(self, commit):
		"""
		Checks if the given commit exists in the project in its full version (including stats and files).

		:param commit: the commit to be checked.
		:returns: True if the given commit exists in the project, or False otherwise.
		"""
		return commit["sha"] in self["commits"] and "stats" in self["commits"][commit["sha"]]

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

	def contributor_exists(self, contributor):
		"""
		Checks if the given commit comment exists in the project.

		:param contributor: the commit comment to be checked.
		:returns: True if the given commit comment exists in the project, or False otherwise.
		"""
		return contributor["id"] in self["contributors"]

	def add_contributor(self, contributor):
		"""
		Adds a contributor to the repository.

		:param contributor: the contributor to be added to the repository.
		"""
		self["contributors"][contributor["id"]] = contributor

	def milestone_exists(self, milestone):
		"""
		Checks if the given commit comment exists in the project.

		:param milestone: the commit comment to be checked.
		:returns: True if the given commit comment exists in the project, or False otherwise.
		"""
		return milestone["id"] in self["milestones"]

	def add_milestone(self, milestone):
		"""
		Adds a milestone to the repository.

		:param milestone: the milestone to be added to the repository.
		"""
		self["milestones"][milestone["id"]] = milestone

	def release_exists(self, release):
		"""
		Checks if the given commit comment exists in the project.

		:param release: the commit comment to be checked.
		:returns: True if the given commit comment exists in the project, or False otherwise.
		"""
		return release["id"] in self["releases"]

	def add_release(self, release):
		"""
		Adds a release to the repository.

		:param release: the release to be added to the repository.
		"""
		self["releases"][release["id"]] = release

	def pull_exists(self, pull):
		"""
		Checks if the given pull request exists in the project.

		:param pull: the pull request to be checked.
		:returns: True if the given pull request exists in the project, or False otherwise.
		"""
		return pull["id"] in self["pulls"]

	def full_pull_exists(self, pull):
		"""
		Checks if the given pull request exists in the project in its full version (including merged_by).

		:param pull: the pull request to be checked.
		:returns: True if the given pull request exists in the project, or False otherwise.
		"""
		if pull["id"] in self["pulls"]:
			return "merged_by" in self["pulls"][pull["id"]]
		else:
			return False

	def add_pull(self, pull):
		"""
		Adds a pull request to the repository.

		:param pull: the pull request to be added to the repository.
		"""
		self["pulls"][pull["id"]] = pull

	def pull_comment_exists(self, pull_comment):
		"""
		Checks if the given pull request comment exists in the project.

		:param pull_comment: the pull request comment to be checked.
		:returns: True if the given pull request comment exists in the project, or False otherwise.
		"""
		return pull_comment["id"] in self["pullComments"]

	def add_pull_comment(self, pull_comment):
		"""
		Adds a pull request comment to the repository.

		:param pull_comment: the pull request comment to be added to the repository.
		"""
		self["pullComments"][pull_comment["id"]] = pull_comment
