#!/usr/bin/env python3

"""
Implementing an expiring web cache and tracker
"""

import requests
import redis
from typing import Callable

# connecting to local Redis server
red = redis.Redis()

def cache(fn: Callable) -> Callable:
	"""
	cache decorator to add caching functionality
	"""
	def wrapper(url):
		"""Wrapper function"""
		# checking if this page has been cached before
		if red.get(url):
			print("Cached data being used...")
			# increment count
			red.incr(f'count:{url}')
			return red.get(url).decode('utf-8')
		else:
			print("Fetching the new data ...")
			result = fn(url)
			# cache the result for 10 seconds
			red.set(url, result, ex=10)
			# initialize the count from 1
			red.set(f'count:{url}', 1)
			return result
	return wrapper

@cache
def get_page(url: str) -> str:
	"""Fetch the HTML content of the url"""
	response = requests.get(url)
	return response.text

# test the function
print(get_page('http://slowwly.robertomurray.co.uk'))
