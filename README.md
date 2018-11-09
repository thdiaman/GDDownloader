GDDownloader: GitHub Data Downloader
====================================
GDDownloader is a data downloader for the GitHub API. The tool allows to download all information
offered for a repository, including commits, issues, commit comments, issue comments, issue events,
as well as the source code of the repository. The tool uses the GitHub API v3, for which more
information can be found [here](https://developer.github.com/v3/).

Prerequisites
-------------
The python library requirements are available in file `requirements.txt` and may be installed using
the command `pip install -r requirements.txt`.

To run this tool, you must have a GitHub account. Also, you must create a GitHub personal access token
(instructions to create one are available [here](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/))
and set it in file `properties.py`. Note that if you also want to access your private repositories you
have to edit the created personal access token and select the repo scope (i.e. Full control of private repositories), and then
you also have to set the variable `include_private_repos` in file `properties.py` to `True`.

Executing the tool
------------------
To run the tool, one must first correctly assign the properties in file `properties.py`.
After that, the tool can be executed by running `python gddownloader.py [github_repo_url_or_list_of_urls]`,
where `github_repo_url_or_list_of_urls` must be replaced by either one of the following:
- a GitHub repo URL (e.g. `https://github.com/thdiaman/GDDownloader`)
- a list of GitHub repo URLs, as a text file where each file is a GitHub repo URL
If a repo already exists in the data folder, then its data are updated.

The main parameters are the following:
- `dataFolderPath`: the path where the data will be downloaded (without trailing slash//backslash)
- `GitHubAuthToken`: your GitHub personal access token (instructions to get one are available [here](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/))
- `gitExecutablePath`: the path to the git executable in your system
- `update_existing_repos`: controls whether the existing (already downloaded) repositories will be updated or skipped
- `verbose`: controls the messages in the standard output (0 for no messages, 1 for simple messages, and 2 for progress bars)
- `always_write_to_disk`: controls whether the repository data will be written to disk on download (always) or after fully downloading them

Controlling what is downloaded
------------------------------
One can also control which data are downloaded by setting the following variables to `True` or `False`:
- `download_issues`
- `download_issue_comments`
- `download_issue_events`
- `download_commits`
- `download_commit_comments`
- `download_contributors`
- `download_source_code`

One can also control whether the full information of issues and commits will be downloaded with the variables
`download_issues_full` and `download_commits_full` respectively. When these variables are set to
`True`, the issues or commits are downloaded one by one (so that all information is included). If they are
set to `False`, then they are downloaded in batches (which is faster but not complete - e.g. the closed_by
field of issues is missing).

Note that the tool does not account for cases when an issue or a commit has already been downloaded (in either
full information or in batch mode) and then has to downloaded again. Issues or commits or any other data that
have already been downloaded are not downloaded again. The tool, however, updates the project when run again for
the same repository by downloading issues, commits, and generally all data that have not already been downloaded.
