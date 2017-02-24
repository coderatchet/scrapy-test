# -*- coding: utf-8 -*-
"""
    test_utils.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

from scrapytest.utils import find_first, merge_dict


def test_find_first_returns_none_on_condition_not_found():
    assert find_first({'foo': 'bar', 'baz': 'spam'}, lambda x, y: False) is None


def test_merge_dict_sees_correct_values():
    a = {'first': {'all_rows': {'pass': 'dog', 'number': '1'}}}
    b = {'first': {'all_rows': {'fail': 'cat', 'number': '5'}}}
    assert merge_dict(b, a) == {'first': {'all_rows': {'pass': 'dog', 'fail': 'cat', 'number': '5'}}}
