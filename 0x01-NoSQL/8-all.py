#!/usr/bin/env python3
"""list all doc nosql"""


import pymongo


def list_all(mongo_collection):
    """return empty if not doc"""
    return [ doc for doc in mongo_collection.find() ]
