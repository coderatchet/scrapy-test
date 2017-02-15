# -*- coding: utf-8 -*-
"""
    test_config.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""


def test_can_read_config_file():
    from scrapytest.config import config
    assert config['mongo_connection_string'] is not None