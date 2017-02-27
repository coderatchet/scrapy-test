# -*- coding: utf-8 -*-
"""
    search.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    keeps the code used for searching the database for articles.

    http://www.apache.org/licenses/LICENSE-2.0
"""
from mongoengine.connection import get_db

from scrapytest.types import Article


class ArticleSearcher:
    """ Object used for searching articles in the database """

    def __init__(self, args: dict):
        self._args = args

    def run(self):
        """ searches the database using the given user arguments """
        # noinspection PyUnresolvedReferences
        print(get_db())
        query_set = Article.objects.search_text(" ".join(self._args['query'])).order_by('$text_score')
        return query_set
