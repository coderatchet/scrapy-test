# -*- coding: utf-8 -*-
"""
    test_db.py

    testing our database code

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""
import logging

import mongoengine
import psutil

from scrapytest.config import config
from scrapytest.types import Article
from pymongo.mongo_client import MongoClient

log = logging.getLogger(__name__)


def test_mongodb_is_up():
    mongod_p = next(x for x in psutil.process_iter() if 'mongod' in x.name())
    if mongod_p is None or not mongod_p.is_running():
        assert False, "mongo db is not currently running!"

try:
    import scrapytest.db
except ImportError as e:
    log.error("Could not load the database connection, is the Mongo service running?")
    exit(1)


def get_test_db_connection():
    return mongoengine.connection.get_connection(alias='test_db')


def test_database_exists():
    _connection = get_test_db_connection()  # type: MongoClient
    assert config['test_db']['db_name'] in _connection.database_names()
    assert _connection.get_default_database().name == config['test_db']['db_name']


# from now on we can reference the connection
connection = get_test_db_connection()


def test_test_data_exists():
    db = connection.get_database(config['test_db']['db_name'])

    # we should have populated the article collection
    assert Article.__name__.lower() in db.collection_names()
    assert db[Article.__name__.lower()].count() > 0
