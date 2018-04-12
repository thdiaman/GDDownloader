import subprocess
import os

class GitDownloader():
	"""
	Class that implements a downloader using the git command.
	"""
	def __init__(self, gitcommand):
		"""
		Initializes this Git Downloader.
		
		:param gitcommand: the path to the git command of the system.
		"""
		self.gitcommand = gitcommand

	def git_pull(self, repo_path):
		"""
		Implements the git pull command.
		
		:param repo_url: the URL of the repository to be pulled.
		:param repo_path: the path of the repository in the file system.
		"""
		subprocess.call([self.gitcommand, 'pull'], cwd = repo_path)

	def git_clone(self, repo_url, repo_path):
		"""
		Implements the git clone command.
		
		:param repo_url: the URL of the repository to be cloned.
		:param repo_path: the path of the file system to clone the repository.
		"""
		subprocess.call([self.gitcommand, 'clone', repo_url, repo_path])

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
