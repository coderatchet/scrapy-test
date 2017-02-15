# -*- coding: utf-8 -*-
"""
    test_types.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""
from scrapytest.types import Article


def test_article_can_create():
    assert Article(1, "introductions", "hello, world", "bob-jones")
