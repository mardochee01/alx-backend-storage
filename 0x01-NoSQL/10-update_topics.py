#!/usr/bin/env python3
"""update topic python"""


def update_topics(mongo_collection, name, topics):
    """name and topics parameter"""
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
