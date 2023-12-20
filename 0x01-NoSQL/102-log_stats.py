#!/usr/bin/env python3

"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""
import re
from pymongo import MongoClient

if __name__ == "__main__":
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

	ip_counts = {}

	all_fields = collection.find({}).limit(10)

	for doc in all_fields:
		ip = doc['ip']
		if ip not in ip_counts:
			ip_counts[ip] = 1
		else:
			ip_counts[ip] += 1

	sorted_ips = sorted(ip_counts.items(), key=lambda item: item[0])

	print("IPs:")
	for ip, count in sorted_ips:
		print(f"\t{ip}: {count}")
