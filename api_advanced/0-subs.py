#!/usr/bin/python3
"""
Module to query subscribers of a given subreddit using Reddit API.
"""

import requests


def number_of_subscribers(subreddit):
    """Returns the number of subscribers for a given subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        return 0
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'alu-scripting:api-advanced:v1.0'}
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        except ValueError:
            return 0
    return 0
