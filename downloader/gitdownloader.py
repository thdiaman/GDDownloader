import os
import subprocess

class GitDownloader():
	"""
	Class that implements a downloader using the git command. To use this class, git must
	be installed in your system.
	"""
	def __init__(self, gitcommand, logger):
		"""
		Initializes this Git Downloader.

		:param gitcommand: the path to the git command of the system.
		:param logger: a Logger used to print messages from git.
		"""
		self.gitcommand = gitcommand
		self.logger = logger

	def git_pull(self, repo_path):
		"""
		Implements the git pull command.

		:param repo_url: the URL of the repository to be pulled.
		:param repo_path: the path of the repository in the file system.
		"""
		p = subprocess.Popen([self.gitcommand, 'pull'], cwd = repo_path, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		while True:
			line = p.stdout.readline()
			if line != b'':
				self.logger.log_action(line.decode('utf-8'))
			else:
				break

	def git_clone(self, repo_url, repo_path):
		"""
		Implements the git clone command.

		:param repo_url: the URL of the repository to be cloned.
		:param repo_path: the path of the file system to clone the repository.
		"""
		p = subprocess.Popen([self.gitcommand, 'clone', repo_url, repo_path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		while True:
			line = p.stdout.readline()
			if line != b'':
				self.logger.log_action(line.decode('utf-8'))
			else:
				break

	def git_repo_exists(self, project_path):
		"""
		Checks if the file system contains a project.

		:param project_path: the path of the project to check if it is a git repo.
		:returns: True if the project has git, or False otherwise.
		"""
		return os.path.isdir(os.path.join(project_path, ".git"))

	def git_pull_or_clone(self, project_id, repo_url, repo_path, repo_branch):
		"""
		Clones a repository or pulls it if it already exists.

		:param project_id: the id of the project to check if it exists in the file system.
		:param repo_url: the URL of the repository to be cloned or pulled.
		:param repo_path: the path of the file system to clone or pull the repository.
		:param repo_branch: the branch to be cloned or pulled.
		"""
		if self.has_project(project_id):
			self.git_pull(repo_url, repo_path, repo_branch)
		else:
			self.git_clone(repo_url, repo_path, repo_branch)
