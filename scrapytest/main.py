# -*- coding: utf-8 -*-
"""
    runner.py

    Copyright 2017 CodeRatchet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
"""
import logging
import os
import sys
from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess

from scrapytest.config import config
from scrapytest.search import ArticleSearcher
from scrapytest.types import Article

log = logging.getLogger(__name__)


class Runner:
    """
    main crawler api.

    usage:
        `./run crawl [OPTIONS...]` will crawl the website and store the articles in the attached database
        `./run search [OPTIONS...]` [EXPRESSION] will search for a given article with the following search expression.
    """

    def __init__(self):

        # setup the parse and its initial values
        self._parser = ArgumentParser(prog=os.path.basename(__file__),
                                      description='Utility for parsing and searching articles on the '
                                                  '\"theguardian.com.au\" website')
        self._configure_parser()
        if len(sys.argv) < 2:
            self._parser.print_usage()
            exit(1)
        self._custom_guardian_config = {}
        self._args = {}

    def run(self):
        # Parse command line args
        parsed_args = self._parser.parse_args()
        self._args = vars(parsed_args)

        # configure the program according to user args
        self._process_arguments()

        # default function according to sub_parser is stored in the func attribute on the Namespace.
        parsed_args.func()
        self._custom_guardian_config = {}  # type: dict

    def search(self):
        """ search the database for the terms defined in the argument to --search/-s """
        # initialize the database
        # noinspection PyUnresolvedReferences
        import scrapytest.db

        log.debug("searching for articles with: '{}'".format(self._args['query']))
        searcher = ArticleSearcher(self._args)
        results = searcher.run()  # type: list[Article]

        result_arr = []
        index = 0

        print("Displaying results from highest rank to lowest:\n")
        for result in results:
            index += 1
            print("{:2d}) {}".format(index, result.title))
            result_arr.append(result)

        # Ask the user for a selection until a valid input is given.
        if index > 0:
            while True:
                try:
                    number = int(input("\nplease choose a number between 1 and {}: ".format(index)))
                    if number < 1 or number > index:
                        raise ValueError
                    else:
                        # Leave some room for viewing clarity then print the article.
                        print("\n")
                        print_article(result_arr[number - 1])
                        break
                except ValueError:
                    print("invalid choice!")
        else:
            print("search yielded no results")

    def crawl(self):
        """ crawl through the database and either save the results to a database or text files. """
        # setup settings
        from scrapy.settings import Settings
        from scrapytest.spiders import GuardianNewsSpider

        settings = Settings()
        settings.set("USER_AGENT", config['crawler_user_agent'])
        settings.set("LOG_LEVEL", self._args['log_level'])
        settings.set('custom_guardian_config', self._custom_guardian_config)

        crawler = CrawlerProcess(settings=settings)
        crawler.crawl(GuardianNewsSpider)
        crawler.start()
        crawler.join()

    def _process_arguments(self):
        """ process and save the effects of command line arguments """
        # log level
        logging.basicConfig(filename=self._args['log_file'], level=self._args['log_level'])
        self._custom_guardian_config['LOG_LEVEL'] = self._args['log_level']
        if 'max_depth' in self._args:
            self._custom_guardian_config.update({'max_depth': self._args['max_depth']})

    def _configure_parser(self):
        """ Add the command line options to the argument parser """
        # All parsers have logging
        self._log_parser = ArgumentParser(add_help=False)
        self._log_parser.add_argument('-l', '--log-level', help="set level of log output", dest='log_level',
                                      action='store', type=str.upper, default='INFO',
                                      choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'])
        self._log_parser.add_argument('-lf', '--log-file', help="set the file for storing log data", dest='log_file',
                                      action='store', type=str, default='./scrapytest.log')

        self._subparsers = self._parser.add_subparsers()

        # setup search api
        self._search_parser = self._subparsers.add_parser('search', help='Search for articles in the database',
                                                          parents=[self._log_parser])  # type: ArgumentParser
        self._search_parser.set_defaults(func=self.search)

        # TODO: Implement functionality
        self._search_parser.add_argument('query', help="search query for finding an article", nargs='+',
                                         action='store', type=str, metavar="QUERY")

        # TODO: add case sensitive search
        # setup crawl api
        self._crawl_parser = self._subparsers.add_parser('crawl',
                                                         help='Crawl through \"theguardian.com.au\" and optionally '
                                                              'store data',
                                                         parents=[self._log_parser])  # type: ArgumentParser
        self._crawl_parser.set_defaults(func=self.crawl)
        self._crawl_parser.add_argument('--section', help="section to search under", dest='section', nargs='+',
                                        choices=config['guardian_spider']['collection_paths'])

        # TODO: Implement functionality
        self._crawl_parser.add_argument('--no-save', help="do not save results to the database",
                                        dest='save_crawl_results',
                                        action='store_false', default=True)

        # TODO: Implement functionality
        self._crawl_parser.add_argument('-p', '--print-json', help="print results in json format", action='store_true',
                                        dest='print_json')


def print_article(article: Article):
    title__format = "Title: {}".format(article.title)
    print(title__format)
    print(("=" * len(title__format)) + "\n")
    print("by: {}, on: {}\n\n".format(article.author, article.date_time))
    print(article.content)


if __name__ == '__main__':
    """ see above """
    runner = Runner()
    try:
        runner.run()
    except Exception as e:
        log.error(e)
