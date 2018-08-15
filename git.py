import re
import yaml
import json
import requests

class GitHubAPI():
    """Fetching user data from GitHub API using issued tokens"""

    def __init__(self, handle):
        self.name = handle

        # Reading token from _config.yml file
        with open("_config.yml", 'r') as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise exc

        # Setting up headers 
        self.headers = {'Authorization' : 'token ' + self.config['token']}
        self.link = "https://api.github.com/users/" + self.name

    def get_data(self):
        """
        Get user data from Gihub API.
        
        @return: User's data. Dict.
        """

        response = requests.get(self.link, headers=self.headers)
        data = response.json()

        public_repos = data['public_repos']
        followers = data['followers']

        # initialising variables.
        stars_recieved = 0
        stars_given = 0
        commits = 0
        size = 0
        open_issues = 0

        resp2 = requests.get("https://api.github.com/users/" + self.name + "/starred?per_page=1", headers=self.headers)
        data2 = resp2.headers

        # cleaning the response headers for starred repositories
        temp = data2['Link']
        temp = temp.split("page=")[-1]
        temp = temp.split(">")[0]

        stars_given = int(temp)

        # Getting all repositories list
        repos_list = []
        for i in range(100):
            resp2 = requests.get("https://api.github.com/users/" + self.name + "/repos?page="+str(i)+"&per_page=100", headers={"Accept":"application/vnd.github.mercy-preview+json", 'Authorization' : 'token ' + self.config['token']})
            data2 = resp2.json()

            repos_list = repos_list + data2
            if len(data2) == 0 or len(data2) < 100:
                break

        languages = []
        topics = []

        # Iterating through repositories and fetching data
        for i in repos_list:
            data3 = requests.get(i["url"]+"/contributors?per_page=100", headers=self.headers).json()

            for k in data3:
                commits+=k["contributions"]

            lang = requests.get(i["languages_url"], headers=self.headers).json()

            for (key, value) in lang.items():
                if key not in languages:
                    languages.append(key)

            for j in i["topics"]:
                if j not in topics:
                    topics.append(j)

            size += i['size']

            stars_recieved += i['stargazers_count']
            open_issues += i['open_issues']


        # storing result in dict format
        result = {
            "stars_recieved": stars_recieved,
            "stars_given": stars_given,
            "commits": commits,
            "size": size,
            "topics": topics,
            "languages": languages,
            "public_repos": public_repos,
            "followers": followers,
            "issues": open_issues
        }

        return result
