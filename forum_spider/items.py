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
    comment_cnt = scrapy.Field()
    comment = scrapy.Field()  # [{text, push, user}] [{text, user}]
    text_seg = scrapy.Field()
    text_pos = scrapy.Field()
    text_ner = scrapy.Field()
    title_seg = scrapy.Field()
    title_pos = scrapy.Field()
    title_ner = scrapy.Field()


class PttItem(BaseItem):
    author_ip = scrapy.Field()
    category = scrapy.Field()
    img_link = scrapy.Field()


class GamerItem(BaseItem):
    board_bsn = scrapy.Field()
    like_cnt = scrapy.Field()
    dislike_cnt = scrapy.Field()


class DcardItem(BaseItem):
    id = scrapy.Field()
    topics = scrapy.Field()
    like_cnt = scrapy.Field()


class M01Item(BaseItem):
    sub_board = scrapy.Field()
