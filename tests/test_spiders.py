# -*- coding: utf-8 -*-
"""
    test_spiders.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""
from scrapy.http import HtmlResponse
from scrapy.http import Response, Request

import os

from scrapy.settings import Settings

from scrapytest.spiders import GuardianNewsSpider

sample_dir = os.path.join(os.path.dirname(__file__), 'guardian_sample_html')


def fake_response_s(text: str, url=None):
    """
    obtained from http://stackoverflow.com/a/12741030/735284

    Create a Scrapy fake HTTP response from a HTML file
    :param str file_name: The relative filename from the responses directory,
                      but absolute paths are also accepted.
    :param str url: The URL of the response.
    :returns: A scrapy HTTP response which can be used for unittesting.
    """
    if not url:
        url = 'http://www.example.com'

    request = Request(url=url)
    response = HtmlResponse(url=url,
                            request=request,
                            body=text, encoding='utf-8')
    return response


def get_sample_contents(file_name: str):
    """
    obtain the contents of the given file from the sample html folder

    :param file_name: file name located in the sample directory
    :return: the string for the file contents
    """
    with open(os.path.join(sample_dir, file_name), 'r') as file:
        return file.read()


def test_author_1():
    spider = GuardianNewsSpider(settings=Settings())
    author_1 = get_sample_contents('author_1.html')
    fake_response = fake_response_s(author_1)
    name = spider._parse_author_tag(fake_response)
    assert name == 'SAMPLE PERSON'
