#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker
"""

import requests
import redis

# connecting to local Redis server
red = redis.Redis()


def get_page(url: str) -> str:
    """Fetch the HTML content of the url and cache value"""

    cached = red.get(f'cached:{url}')
    if cached is not None:
        red.incr(f'count:{url}')
        return cached.decode('utf-8')
    else:
        response = requests.get(url)
        red.setex(f'cached:{url}', 10, response.text)
        red.set(f'cached:{url}', 1)
        return response.text
