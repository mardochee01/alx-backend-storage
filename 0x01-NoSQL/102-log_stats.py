#!/usr/bin/env python3
"""log stats new version"""
from pymongo import MongoClient

if __name__ == "__main__":
    """Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    nginx_logs = nginx_collection.count_documents({})
    print(f'{nginx_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    status = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )

    print(f'{status} status check')

    ips = nginx_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    print("IPs:")
    for ip in ips:
        result = ip.get("result")
        count = ip.get("count")
        print(f'\t{result}: {count}')
