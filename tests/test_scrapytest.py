# -*- coding: utf-8 -*-
"""
    scrapytest.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

import pytest
from scrapytest import __version_info__, __version__


def test_version_info():
    assert isinstance(__version_info__, tuple)


def test_version_string():
    assert isinstance(__version__, str)
