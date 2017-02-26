# -*- coding: utf-8 -*-
"""
    db.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""
import mongoengine
from mongoengine import connect
from pymongo.errors import BulkWriteError

from .config import config
from .types import Article


def construct_connection_string(db: str):
    return "mongodb://{host}:{port}/{db_name}".format_map({**{
        # These default parameters are overridden by the config.json contents of key "db"
        "host": "localhost",
        "port": "27017",
        "db_name": "test"
    }, **config[db]})


db_connection_string = construct_connection_string("db")
connect(host=db_connection_string, alias="default")

# load test data if applicable
if config.get('load_test_data', False):
    import os

    "connect to the test database"
    test_db_connection_string = construct_connection_string("test_db")
    mongoengine.connection.register_connection(host=test_db_connection_string, alias="test_db")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

    with open(os.path.join(root_dir, config['test_data_file'])) as file:
        import json

        data = json.loads(file.read())
        try:
            Article.switch_db(db_alias='test_db').drop_collection()
        except BulkWriteError as e:
            print(e.details)
        finally:
            # iterate through articles and persist them.
            for article in data:
                new_article = Article(title=article['title'],
                                      author=article['author'],
                                      content=article.get('content', None)).switch_db(db_alias="test_db")
                new_article.save()
