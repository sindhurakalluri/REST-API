import requests

class BitbucketAPI():
    """Fetching handle (team or user) data from Bitbucket public API"""

    def __init__(self, handle):
        self.handle = handle
        self.baseurl = "https://api.bitbucket.org/2.0/"

    def get_data(self):
        """
        Get user data from Bitbucket API.
        
        @return: User's data. Dict.
        """

        resp = requests.get(self.baseurl + "users/" + self.handle)
        data = resp.json()
        # Fetching user response

        if data['type'] == 'error':
            resp = requests.get(self.baseurl + "teams/" + self.handle)
            data = resp.json()

        followers_count = 0

        # iterating through pages to count number of followers
        link1 = data['links']['followers']['href'] + "?pagelen=100"
        while True:
            resp1 = requests.get(link1).json()
            followers_count += len(resp1['values'])

            if "next" not in resp1:
                break
            else:
                link1 = resp1['next']

        # initialising values needed
        repos_count = 0
        size = 0
        languages = []
        commits = 0
        issues = 0

        # iterating through repositories and fetching data
        link2 = data['links']['repositories']['href'] + "?pagelen=100"
        while True:
            resp2 = requests.get(link2).json()
            repos_count += len(resp2['values'])

            for repo in resp2['values']:
                size += repo['size']

                if repo['language'] not in languages:
                    languages.append(repo['language'])

                commitsurl = repo['links']['commits']['href']+"?pagelen=100"
                while True:
                    resp3 = requests.get(commitsurl).json()

                    commits += len(resp3['values'])
                    if 'next' not in resp3:
                        break
                    else:
                        commitsurl = resp3['next']

                issuesurl = repo['links']['self']['href'] + "/issues"
                try:
                    resp4 = requests.get(issuesurl).json()
                    issues += resp4['size']
                except Exception as e:
                    issues += 0

            if "next" not in resp2:
                break
            else:
                link2 = resp2['next']

        # formatting result into dict format
        result = {
        "followers": followers_count,
        "public_repos": repos_count,
        "size": size,
        "commits": commits,
        "languages": languages,
        "issues": issues,
        "topics": [],
        "stars_recieved": 0,
        "stars_given": 0
        }

        return result


if __name__=="__main__":
    r = BitbucketAPI("techcentaur").get_data()
    print(r)