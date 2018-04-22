import json

def get_number_of(gdownloader, repo_api_address, statistic_type, parameter = None):
	"""
	Posts a request using an instance of GithubDownloader and returns the number of
	a given statistic (e.g. number of issues, number of commits, etc.).

	:param gdownloader: an instance of GithubDownloader.
	:param statistic_type: the type for which the statistic is downloaded.
	:param parameter: an optional parameter for the statistic (e.g. for issues set this to "state=all" to get all of them).
	:returns: the value for the statistic as an absolute number.
	"""
	r = gdownloader.download_request(repo_api_address + "/" + statistic_type, ["per_page=100"] if parameter == None else ["per_page=100", parameter])
	if "link" in r.headers:
		address = r.headers["link"].split(',')[1].split('<')[1].split('>')[0]
		data = gdownloader.download_object(address)
		return 100 * (int(address.split('=')[-1]) - 1) + len(data)
	else:
		data = json.loads(r.text or r.content)
		return len(data)

def read_file_in_lines(filename):
	"""
	Reads a file into lines.

	:param filename: the filename of the file to be read.
	:returns: a list with the lines of the file.
	"""
	with open(filename) as infile:
		lines = infile.readlines()
	return lines

def print_usage():
	"""
	Prints the usage information of this python file.
	"""
	print("Usage: python gddownloader.py arg")
	print("where arg can be one of the following:")
	print("   github url (e.g. https://github.com/user/repo)")
	print("   path to txt file containing github urls")

