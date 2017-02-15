#!/usr/bin/python
# -*- coding: utf-8 -*- #
"""
    setup.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""

from setuptools import setup, find_packages
from scrapytest import __version__

import sys
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(
    name="scrapytest",
    version=__version__,
    description='A Test for assessing developer\'s proficiency',
    url='https://github.com/coderatchet/scrapt-test.git',
    long_description=open("README.md").read(),
    download_url='https://github.com/coderatchet/scrapytest/archive/' + __version__ + '.tar.gz',
    license='Apache 2.0',
    author='CodeRatchet',
    author_email='coderatchet@gmail.com',
    maintainer='Jared Nagle',
    maintainer_email='coderatchet@gmail.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['scrapy>=1.3.2', 'BeautifulSoup4>=4.5.3', 'pyasn1', 'pymongo', 'mongoengine'],
    tests_require=['pytest'],

    # empty array for now
    setup_requires=[] + pytest_runner
)
