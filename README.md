## REST-API for aggregate data from Github and Bitbucket APIs

## Configuration
Edit the `token` variable in `_config.yml` file with a token from GitHub.
```yml
token: <put-your-token-here>
```
- GitHub provides 60 public API calls per hour; it is plausible that we need more calls than this, so, put a personal token in the `_config.yml` file to increase the API calls upto 5000 per hour.
- BitBucket provides a large number of free API calls so a personal token for it is not necessary.

## Run
- Run `python3 app.py` to run the flask web-app.
```console
HAL@Sumit:~$ python3 app.py 
* Serving Flask app "app" (lazy loading)
* Environment: production
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
	- Use REST API as `http://127.0.0.1:5000/username?git=<github_handle>&bit=<bitbucket_handle>`

- Run `pytest` to test the independent `git.py` and `bit.py` python files.

## Usage

For `git.py` -

```console
>>> import git
>>> githubapi = git.GitHubAPI("Nishkarsh5")
>>> githubapi.get_data()
{'stars_recieved': 0, 'stars_given': 13, 'commits': 13, 'size': 8, 'topics': [], 'languages': ['Python'], 'public_repos': 1, 'followers': 1, 'issues': 0}
```

Similarly for `bit.py` - 

```console
>>> import bit
>>> bitapi = bit.BitbucketAPI("techcentaur")
>>> bitapi.get_data()
{'followers': 0, 'public_repos': 0, 'size': 0, 'commits': 0, 'languages': [], 'issues': 0, 'topics': [], 'stars_recieved': 0, 'stars_given': 0}
```
