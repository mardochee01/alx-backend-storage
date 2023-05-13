#!/usr/bin/env python3
"""insert pyhton mongo"""


def insert_school(mongo_collection, **kwargs):
    """return _id"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
