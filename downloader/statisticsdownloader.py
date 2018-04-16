import json

class StatisticsDownloader:
	"""
	Class that implements a statistics downloader for the GitHub API.
	"""

	def __init__(self, gdownloader):
		"""
		Initializes this GitHub statistics Downloader.
		
		:param gdownloader: an instance of GitHubDownloader.
		"""
		self.gdownloader = gdownloader

	def get_number_of_commits(self, repo_name):
		"""
		Returns the number of commits given the name of a GitHub repo.
		
		:param repo_name: the name of the repo in the format user/repo.
		:returns: an integer denoting the number of commits in the given repo.
		"""
		r = self.gdownloader.download_request("https://api.github.com/repos/" + repo_name + "/issues", ["per_page=100"])
		if "link" in r.headers:
			address = r.headers["link"].split(',')[1].split('<')[1].split('>')[0]
			data = self.gdownloader.download_object(address)
			return 100 * (int(address.split('=')[-1]) - 1) + len(data)
		else:
			data = json.loads(r.text or r.content)
			return len(data)
	
	def get_number_of_issues(self, repo_name):
		"""
		Returns the number of issues given the name of a GitHub repo.
		
		:param repo_name: the name of the repo in the format user/repo.
		:returns: an integer denoting the number of issues in the given repo.
		"""
		r = self.gdownloader.download_request("https://api.github.com/repos/" + repo_name + "/issues", ["per_page=100", "state=all"])
		if "link" in r.headers:
			address = r.headers["link"].split(',')[1].split('<')[1].split('>')[0]
			data = self.gdownloader.download_object(address)
			return 100 * (int(address.split('=')[-1]) - 1) + len(data)
		else:
			data = json.loads(r.text or r.content)
			return len(data)
