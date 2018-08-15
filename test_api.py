import git, bit


def test_function_for_githubAPI():
    result = data_git = git.GitHubAPI("Nishkarsh5").get_data()

    result_predicted = {'stars_recieved': 0,
        'stars_given': 13,
        'commits': 13,
        'size': 8,
        'topics': [],
        'languages': ['Python'],
        'public_repos': 1,
        'followers': 1,
        'issues': 0
    }

    assert result == result_predicted

def test_function_for_bitbucketAPI():
    result = bit.BitbucketAPI("techcentaur").get_data()

    result_predicted = {'followers': 0,
        'public_repos': 0,
        'size': 0,
        'commits': 0,
        'languages': [],
        'issues': 0,
        'topics': [],
        'stars_recieved': 0,
        'stars_given': 0
    }

    assert result == result_predicted