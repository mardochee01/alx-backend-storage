#!/usr/bin/env python3
"""log statt"""


from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx

    docs_num = logs.count_documents({})
    get_num = logs.count_documents({'method': 'GET'})
    post_num = logs.count_documents({'method': 'POST'})
    put_num = logs.count_documents({'method': 'PUT'})
    patch_num = logs.count_documents({'method': 'PATCH'})
    delete_num = logs.count_documents({'method': 'DELETE'})
    status = logs.count_documents({'method': 'GET', 'path': '/status'})
    print("{} logs".format(docs_num))
    print("Methods:")
    print("\tmethod GET: {}".format(get_num))
    print("\tmethod POST: {}".format(post_num))
    print("\tmethod PUT: {}".format(put_num))
    print("\tmethod PATCH: {}".format(patch_num))
    print("\tmethod DELETE: {}".format(delete_num))
    print("{} status check".format(status))
