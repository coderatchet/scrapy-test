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
from mongoengine import Q
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
        query_set = Article.objects(self.construct_query())
        return query_set

    def construct_query(self):
        """
        combines all terms found on the expression into a single query
        :return Q: the full query to be passed to the objects method of the Article
        """
        search_expression = self._args['query']
        return Q(content__icontains=search_expression[0]) | Q(title__icontains=search_expression[0])
