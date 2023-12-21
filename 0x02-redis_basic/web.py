#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker
"""

import requests
import redis

# connecting to local Redis server
red = redis.Redis()
count = 0


def get_page(url: str) -> str:
    """Fetch the HTML content of the url and cache value"""

    red.set(f'cached:{url}', count)
    response = requests.get(url)
    red.incr(f'count:{url}')
    red.setex(f'cached:{url}', 10, red.get(f'cached:{url}'))
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
