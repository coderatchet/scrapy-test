import logging
import re
from datetime import datetime

import scrapy
from scrapy.http import Response

# noinspection PyUnresolvedReferences
import scrapytest.db
from scrapytest.config import config
from scrapytest.types import Article
from scrapytest.utils import merge_dict

log = logging.getLogger(__name__)


class GuardianNewsSpider(scrapy.spiders.CrawlSpider):
    """ Spider that crawls over the Guardian news website"""
    name = "guardian"

    _user_config = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, '_user_config'):
            self._config = merge_dict(self._user_config, config['guardian_spider'])
        else:
            self._config = config['guardian_spider']

    @classmethod
    def update_settings(cls, settings):
        super(GuardianNewsSpider, cls).update_settings(settings)

        # super impose user cmd line args onto the current spider configuration.
        if 'custom_guardian_config' in settings:
            cls._user_config = settings.get('custom_guardian_config')

    def start_requests(self):
        """
        generator for requesting the content from each of the main news collection entry points
        """
        urls = ['http://{host}/{path}'.format(host=self._config['host'], path=path) for path in
                self._config['collection_paths']]
        for url in urls:
            max_depth = self._config['max_depth']
            yield scrapy.Request(url=url, callback=lambda response: self._parse_news_list(response, max_depth))

    def _parse_news_list(self, response: Response, depth=10):
        """
        handle the raw html
        :param depth: maximum depth we should search for articles
        :param response: the top level news response
        """
        log.debug("Parsing news list link: {}".format(response.url))
        for link in self._article_links(response):
            link = response.urljoin(link)
            yield scrapy.Request(url=link, callback=self._parse_article_link)
        # if next link exists and depth not exceeded, visit next link and yield results.
        next_page = response.css(self._config['next_page_selector']).extract_first()

        # we keep iterating through until our maximum depth is reached.
        if next_page is not None and depth > 0:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=lambda list_response: self._parse_news_list(list_response,
                                                                                                     depth - 1))

    def _parse_article_link(self, article: Response):
        """
        parses the article's main page

        :param Response article: top level article page.
        should search for existing article and store if not found.
        """
        import re

        # some author elements have clickable links with the name and picture of author
        author_raw = article.css(self._config['author_selector'])
        log.debug("author_raw: {}".format(author_raw.extract_first()))
        try:
            if author_raw.css('a').extract_first() is not None:
                author = author_raw.css('a::text').extract_first()
            else:
                author = author_raw.css('*::text').extract_first()
            author = re.split(r"-", author)[0].strip()
        except:
            author = "The Guardian"

        log.debug("parsed author name: {}".format(author))

        # author is in format of "name - email"
        date_time_string = article.css(self._config['date_time_selector']).extract_first()

        # remove the ':' from the date string as sftptime does not support this
        sub = re.sub(r':([0-9]{2})$', r'\1', date_time_string)
        date_time = datetime.strptime(sub, self._config['date_time_format'])

        # assemble the article object
        title = article.css(self._config['title_selector']).extract_first().strip()

        data = {
            'title': title,
            'author': author,
            'date_time': date_time,
            'content': '\n'.join(article.css(self._config['content_selector']).extract()).strip()
        }

        # persist it if it doesn't exist yet
        log.debug("Searching for existing article with the title '{}' and date_time '{}'".format(title, date_time))
        existing_article = Article.objects(title__exact=title, date_time__exact=date_time).first()

        if existing_article is None:
            log.debug("Article not found for {} - {}, saving new article: {}".format(title, date_time, data))
            new_article = Article(**data)
            new_article.save()
        else:
            log.debug("Article found, not saving")

    @staticmethod
    def _parse_author_tag(author_tag: Response):
        """
        parse the author section for the name
        :param author_tag: the author/div tag to parse
        :return: the name of the author
        """
        text = author_tag.css('.story-header__author-name::text').extract_first()
        return re.split(r"-", text)[0].strip()

    def _article_links(self, news_list_response: Response):
        """
        Generator for iterating through articles

        :param scrapy.http.Response news_list_response: a top level news list page
        :yields: the next article in the news list
        """
        for article_link in news_list_response.css(self._config['article_list_item_link_selector']):
            yield article_link.extract()
