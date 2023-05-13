#!/usr/bin/env python3
"""select by"""


def schools_by_topic(mongo_collection, topic):
    """return list"""
    documents = mongo_collection.find({"topics": topic})
    return [filtre for filtre in documents]
