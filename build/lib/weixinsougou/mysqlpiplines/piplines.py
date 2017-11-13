#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by master on 2017/5/14
from weixinsougou.items import ArticleItem
from .sql import Sql


class AccountPipeline(object):
    def process_item(self, item, spider):

        if isinstance(item, ArticleItem):
            article_title = item['article_title']
            ret = Sql.select_article_title(article_title)
            if ret[0] == 1:
                print('已经存在！')
            else:
                Sql.insert_article(item['account_name'], item['account_id'],
                                   item['article_title'], item['article_digest'],
                                   item['article_url'], item['article_content'],
                                   item['article_cover'], item['article_post_date'])
        return item
