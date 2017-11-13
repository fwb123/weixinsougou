# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    account_name = scrapy.Field()
    account_id = scrapy.Field()
    article_title = scrapy.Field()
    article_digest = scrapy.Field()
    article_url = scrapy.Field()
    article_content = scrapy.Field()
    article_cover = scrapy.Field()
    article_post_date = scrapy.Field()
