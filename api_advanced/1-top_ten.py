#!/usr/bin/python3
"""
Module that queries the Reddit API and prints
the titles of the first 10 hot posts.
"""

import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a given subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {'User-Agent': 'custom-user-agent/1.0'}
    
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            if not posts:
                print(None)
                return
            for post in posts:
                print(post.get('data', {}).get('title'))
        else:
            print(None)
    except Exception:
        print(None)
