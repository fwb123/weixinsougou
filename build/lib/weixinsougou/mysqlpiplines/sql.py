#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by master on 2017/5/14

import pymysql as mysql

from weixinsougou import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB
MYSQL_CHARSET = settings.MYSQL_CHARSET

conn = mysql.connect(user=MYSQL_USER,
                     password=MYSQL_PASSWORD,
                     host=MYSQL_HOSTS,
                     database=MYSQL_DB,
                     charset=MYSQL_CHARSET)
cursor = conn.cursor()


class Sql(object):
    '''
             DROP TABLE IF EXISTS zfs_wechat_article;
                CREATE TABLE zfs_wechat_article (
                id int(11) NOT NULL AUTO_INCREMENT,
                account_name varchar(255) DEFAULT NULL,
                account_id varchar(255) DEFAULT NULL,
                article_title varchar(255) DEFAULT NULL,
                article_digest varchar(255) DEFAULT NULL,
                article_url varchar(255) DEFAULT NULL,
                article_content MEDIUMTEXT DEFAULT NULL,
                article_cover varchar(255) DEFAULT NULL,
                article_post_date varchar(255) DEFAULT NULL,
                PRIMARY KEY (id)
                ) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4;
    '''

    @staticmethod
    def insert_article(account_name, account_id, article_title, article_digest, article_url,article_content, article_cover,
                       article_post_date):
        sql = '''
                    INSERT INTO zfs_wechat_article (account_name,account_id,article_title,article_digest,article_url,article_content,article_cover,
                    article_post_date) VALUES (%(account_name)s,%(account_id)s,%(article_title)s,%(article_digest)s,%(article_url)s,%(article_content)s,%(article_cover)s,%(article_post_date)s)
            '''

        value = {
            'account_name': account_name,
            'account_id': account_id,
            'article_title': article_title,
            'article_digest': article_digest,
            'article_url': article_url,
            'article_content': article_content,
            'article_cover': article_cover,
            'article_post_date': article_post_date,
        }
        cursor.execute(sql, value)
        conn.commit()

    @staticmethod
    def select_article_title(article_title):
        sql = '''
                SELECT EXISTS(SELECT 1 FROM zfs_wechat_article WHERE article_title=%(article_title)s)
            '''
        value = {
            'article_title': article_title
        }

        cursor.execute(sql, value)
        return cursor.fetchall()[0]

    # 错误处理方法
    @staticmethod
    def _handle_error(failure, item, spider):
        print(failure)
