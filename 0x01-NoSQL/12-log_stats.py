#!/usr/bin/env python3

"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017')


db = client["logs"]
collection = db["nginx"]

total_logs = collection.count_documents({})
print(f"{total_logs} logs")
print("Methods:")
Methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for no_docs in Methods:
	count = collection.count_documents({"method": no_docs})
	print(f"\tmethod {no_docs}: {count}")

status_count = collection.count_documents({"method": "GET", "path": "/status"})
print(f"{status_count} status check")
