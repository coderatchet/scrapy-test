# -*- coding: utf-8 -*-
"""
    db.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from .config import config

# would use constants here but short for time.
client = MongoClient(config['mongo_connection_string'])
db = client[config['db_name']]
articles = db.articles

# load test data if applicable
if config.get('load_test_data', False):
    import os

    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    with open(os.path.join(root_dir, config['test_data_file'])) as file:
        import json

        data = json.loads(file.read())
        try:
            if 'articles' in db.collection_names():
                db.drop_collection('articles')
            articles.insert_many(data)
        except BulkWriteError as e:
            print(e.details)
