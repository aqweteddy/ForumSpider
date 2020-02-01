# -*- coding: utf-8 -*-
import json
from datetime import datetime
from urllib.parse import urlencode

import scrapy

from forum_spider.items import DcardItem
from forum_spider.spiders.custom_settings import combine_settings


class DcardSpider(scrapy.Spider):
    name = 'dcard'
    allowed_domains = ['dcard.tw']
    custom_settings = combine_settings(name)

    def __init__(self, board: list, max_page: int, popular=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.max_page = max_page
        self.popular = popular

    def start_requests(self):
        for board in self.board:
            key = urlencode({'popular': str(self.popular).lower()})
            if board == 'hot':
                url = f'https://dcard.tw/_api/posts?{key}'
            else:
                url = f'https://dcard.tw/_api/forums/{board}/posts?{key}'
            yield scrapy.Request(url, meta={'times': 1, 'url': url})

    def parse(self, resp):
        result = json.loads(resp.body_as_unicode())
        last_id = 0

        for data in result:
            item = DcardItem()
            item['id'] = data['id']
            item['board'] = data['forumAlias']
            item['topics'] = data['topics']
            item['title'] = data['title']
            item['comment_cnt'] = data['commentCount']
            item['forum'] = 'dcard'
            item['create_date'] = datetime.strptime(data['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
            item['last_update_date'] = item['create_date']
            item['like_cnt'] = data['likeCount']
            yield scrapy.Request(f'https://dcard.tw/_api/posts/{data['id']}',
                                 callback=self.parse_post,
                                 meta={ 'item': item })
            last_id = item['id']

        if self.max_page < resp.meta['times'] and len(result) != 0:
            yield scrapy.Request(f'{resp.meta['url']}&before={last_id}',
                                 callback=self.parse,
                                 meta={'times': resp.meta['times'] + 1,
                                       'url': resp.meta['url']}
                                 )

    def parse_post(self, resp):
        result = json.loads(resp.body_as_unicode())
        item = resp.meta['item']

        item['url'] = 'www.dcard.tw/f/{}/p/{}'.format(item['board'], item['id'])
        item['text'] = result.get('content', '')
        yield scrapy.Request('https://dcard.tw/_api/posts/{}/comments'.format(item['id']),
                             meta={'item': item},
                             callback=self.parse_comment
                             )

    def parse_comment(self, resp):
        result = json.loads(resp.body_as_unicode())
        item = resp.meta['item']
        item['comment'] = [{
            'text': data.get('content', ''),
            'like_cnt': data.get('likeCount')
        } for data in result]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        yield item
