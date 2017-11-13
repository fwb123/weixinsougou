#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by master on 2017/5/13
import json
import re

from lxml import etree

import scrapy
from scrapy.http import Request

from weixinsougou.items import ArticleItem


group_ids = [
    'P0S100',
    'paycircle',
    'payshot',
    'payworld',
    'zhifubaoliao',
    'zhifuquaner',
    'zhifuzhijiawang',
    'baoliaomi',
    'Paypedia',
    'mpaypass',
    'zhifuquanzi',
]


class WechatSpider(scrapy.Spider):
    name = 'Weixinsougou'
    base_url = 'http://mp.weixin.qq.com'

    allowed_domains = ['weixin.sougou.com']

    def start_requests(self):  # 入口函数 名字必须是这个
        for group_id in group_ids:
            url = 'http://weixin.sogou.com/weixinwap?query=' + group_id
            yield Request(url, self.parse, dont_filter=True)

    def parse(self, response):
        page = etree.HTML(response.text)
        account_url = page.xpath('//div[@class="gzh-box"]/a/@href')[0]
        account_name = page.xpath('//p[@class="gzh-tit"]/text()')[0]
        account_id = page.xpath('//p[@class="gzh-name"]/text()')[0]
        account_intro = page.xpath('//dd/text()')[0]
        account_owner = page.xpath('//dd/text()')[1]

        account_info = {'account_name': account_name, 'account_id': account_id, 'account_url': account_url,
                        'account_intro': account_intro, 'account_owner': account_owner}
        yield Request(account_url, callback=self.parse_article, dont_filter=True, meta={'account_info': account_info})

    def parse_article(self, response):
        page = etree.HTML(response.text)
        js_content = page.xpath('//script')[-2].text
        json_article = re.search('{"list":[\s\S]*}', js_content).group()
        data = json.loads(json_article, encoding='utf-8')
        list_articles = []
        for item in data['list']:
            article_post_date = item['comm_msg_info']['datetime']
            article_url = self.base_url + item['app_msg_ext_info']['content_url'].replace('amp;', '')
            article_cover = item['app_msg_ext_info']['cover']
            article_digest = item['app_msg_ext_info']['digest']
            article_title = item['app_msg_ext_info']['title']

            article_item = ArticleItem()

            article_item['account_name'] = response.meta['account_info']['account_name']
            article_item['account_id'] = response.meta['account_info']['account_id']
            article_item['article_title'] = article_title
            article_item['article_digest'] = article_digest
            article_item['article_url'] = article_url
            article_item['article_cover'] = article_cover
            article_item['article_post_date'] = article_post_date
            # article_item['article_content'] = ''
            # yield article_item
            yield Request(article_url, callback=self.article_source, dont_filter=True, meta={'article': article_item})
            list_articles.append(
                {'title': article_title, 'url': article_url, 'cover': article_cover, 'digest': article_digest,
                 'date': article_post_date})
            for sub_item in item['app_msg_ext_info']['multi_app_msg_item_list']:
                article_post_date = item['comm_msg_info']['datetime']
                article_url = self.base_url + sub_item['content_url'].replace('amp;', '')
                article_cover = sub_item['cover']
                article_digest = sub_item['digest']
                article_title = sub_item['title']

                sub_article_item = ArticleItem()
                sub_article_item['account_name'] = response.meta['account_info']['account_name']
                sub_article_item['account_id'] = response.meta['account_info']['account_id']
                sub_article_item['article_title'] = article_title
                sub_article_item['article_digest'] = article_digest
                sub_article_item['article_url'] = article_url
                sub_article_item['article_cover'] = article_cover
                sub_article_item['article_post_date'] = article_post_date
                # sub_article_item['article_content'] = ''
                # yield sub_article_item
                yield Request(article_url, callback=self.article_source, dont_filter=True,
                              meta={'article': sub_article_item})

                list_articles.append(
                    {'title': article_title, 'url': article_url, 'cover': article_cover, 'digest': article_digest,
                     'date': article_post_date})
        account_info = response.meta['account_info']
        account = {'account_info': account_info, "article_list": list_articles}
        # print(account)

    def article_source(self, response):
        page = etree.HTML(response.text)
        image_urls = page.xpath('//img/@data-src')
        img_tags = page.xpath('//img[@data-src]')
        for i in range(len(image_urls)):
            img_tags[i].set('src', image_urls[i])
        # etree.ElementTree(page).write('response.html', pretty_print=True)
        article = response.meta['article']
        article['article_content'] = etree.tostring(page).decode('utf-8')
        yield article
