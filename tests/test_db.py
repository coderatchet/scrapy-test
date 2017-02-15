# -*- coding: utf-8 -*-
"""
    test_db.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""
import psutil
from scrapytest.config import config
from scrapytest.db import client, db


def test_mongodb_is_up():
    mongod_p = next(x for x in psutil.process_iter() if 'mongod' in x.name())
    if mongod_p is None or not mongod_p.is_running():
        assert False, "mongo db is not currently running!"


def test_database_exists():
    assert config['db_name'] in client.database_names()


def test_test_data_exists():
    assert 'articles' in db.collection_names()
    assert db.articles.count() > 0

