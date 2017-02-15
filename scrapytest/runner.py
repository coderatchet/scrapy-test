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

from scrapy.crawler import CrawlerProcess


def main():
    from scrapy.settings import Settings
    from scrapytest.guardian_news_spider import GuardianNewsSpider

    from scrapytest.config import config

    def _spider_closing(spider):
        """Activates on spider closed signal"""
        logging.log("Closing reactor", level=logging.INFO)

    settings = Settings()
    settings.set("USER_AGENT", config['crawler_user_agent'])
    crawler = CrawlerProcess(settings=settings)
    # stop reactor when spider closes
    crawler.crawl(GuardianNewsSpider)
    crawler.start()
    crawler.join()

if __name__ == '__main__':
    main()