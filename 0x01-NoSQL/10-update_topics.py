#!/usr/bin/env python3

"""
Python function that changes all topics of a school document based on the name
"""

from typing import List

def update_topics(mongo_collection, name: str, topics: List[str]):
	"""
	mongo_collection will be the pymongo collection object
	name (string) will be the school name to update
	topics (list of strings) will be the list of topics approached in the school
	"""

	query = {"name": name}
	new_values = {"$set": { "topics": topics}}

	changed_topics = mongo_collection.update_many(query, new_values)
	return changed_topics
