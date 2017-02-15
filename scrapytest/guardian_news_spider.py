import logging
import scrapy

from scrapytest.config import config


class GuardianNewsSpider(scrapy.Spider):
    """ Spider that crawls over the Guardian news website"""
    name = "guardian"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._config = config['guardian_spider']

    def start_requests(self):
        """
        generator for requesting the content from each of the main news collection entry points
        :param url:
        :return:
        """
        logging.basicConfig()
        logging.log(logging.INFO, "here")
        urls = ['http://' + self._config['host'] + path for path in self._config['collection_paths']]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ handle the raw html """
        logging.log(logging.INFO, response)
