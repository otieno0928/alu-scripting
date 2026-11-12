#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the title
of all hot articles, and prints a sorted count of given keywords.
"""

import re
import requests


def count_words(subreddit, word_list, hot_list=None, after=None, counts=None):
    """Recursively counts keyword occurrences in hot article titles."""
    if hot_list is None:
        hot_list = []
    if counts is None:
        counts = {}
        for word in word_list:
            w = word.lower()
            counts[w] = counts.get(w, 0) + 1

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'alu-scripting:api-advanced:v1.0'}
    params = {'after': after} if after else {}
    response = requests.get(
        url, headers=headers, params=params, allow_redirects=False
    )

    if response.status_code != 200:
        if after is None:
            return
        process_and_print(hot_list, counts)
        return

    data = response.json()
    children = data.get('data', {}).get('children', [])
    for child in children:
        hot_list.append(child.get('data', {}).get('title'))

    after = data.get('data', {}).get('after')
    if after is not None:
        return count_words(subreddit, word_list, hot_list, after, counts)

    process_and_print(hot_list, counts)


def process_and_print(hot_list, counts):
    """Processes hot list titles and prints sorted word counts."""
    word_count = {word: 0 for word in counts}

    for title in hot_list:
        words_in_title = re.findall(r'\b[A-Za-z]+\b', title)
        for w in words_in_title:
            w_lower = w.lower()
            if w_lower in word_count:
                word_count[w_lower] += counts[w_lower]

    filtered = {k: v for k, v in word_count.items() if v > 0}
    sorted_words = sorted(filtered.items(), key=lambda x: (-x[1], x[0]))

    for word, cnt in sorted_words:
        print("{}: {}".format(word, cnt))
