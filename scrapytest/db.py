# -*- coding: utf-8 -*-
"""
    db.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

from mongoengine import connect
from pymongo.errors import BulkWriteError

from .types import Article
from .config import config
connection = connect(host="{}/{}".format(config['mongo_connection_string'], config['db_name']))

# load test data if applicable
if config.get('load_test_data', False):
    import os

    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    with open(os.path.join(root_dir, config['test_data_file'])) as file:
        import json

        data = json.loads(file.read())
        try:
            Article.drop_collection()
        except BulkWriteError as e:
            print(e.details)
        finally:
            # iterate through articles and persist them.
            for article in data:
                new_article = Article(title=article['title'],
                        author=article['author'],
                        content=article.get('content', None))
                new_article.save()

