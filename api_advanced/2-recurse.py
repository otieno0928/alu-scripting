#!/usr/bin/python3
"""
Recursive function that queries the Reddit API and returns a list
containing the titles of all hot articles for a given subreddit.
"""

import requests


def recurse(subreddit, hot_list=[], after=None):
    """Recursively fetches all hot article titles for a given subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'alu-scripting:api-advanced:v1.0'}
    params = {'after': after} if after else {}
    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False
    )

    if response.status_code != 200:
        return hot_list if hot_list else None

    data = response.json()
    children = data.get('data', {}).get('children', [])
    for child in children:
        hot_list.append(child.get('data', {}).get('title'))

    after = data.get('data', {}).get('after')
    if after is not None:
        return recurse(subreddit, hot_list, after)
    return hot_list if hot_list else None
