#!/usr/bin/env python3

"""
Python function that lists all documents in a collection
"""

def list_all(mongo_collection):
	"""
	Function that lists all documents in a collection
	Return an empty list if no document in the collection
	"""
	if mongo_collection is None:
		return []
	docs = []
	for x in mongo_collection.find():
		docs.append(x)
	return docs

