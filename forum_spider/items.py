# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    forum = scrapy.Field()
    text = scrapy.Field()
    board = scrapy.Field()
    author = scrapy.Field()
    url = scrapy.Field()
    create_date = scrapy.Field()
    last_update_date = scrapy.Field()
    ws_pos = scrapy.Field()
    ner = scrapy.Field()


class PttItem(BaseItem):
    author_ip = scrapy.Field()
    comment = scrapy.Field()  # [{text, push, user}]
    comment_cnt = scrapy.Field()
    category = scrapy.Field()
    img_link = scrapy.Field()


class GamerItem(BaseItem):
    reply = scrapy.Field()
    comment = scrapy.Field()


class DcardItem(BaseItem):
    comment = scrapy.Field()
    id = scrapy.Field()
    topics = scrapy.Field()
    comment_cnt = scrapy.Field()
    like_cnt = scrapy.Field()
