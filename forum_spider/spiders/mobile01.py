# -*- coding: utf-8 -*-
import scrapy
from forum_spider.items import M01Item
from forum_spider.spiders.custom_settings import combine_settings


class Mobile01Spider(scrapy.Spider):
    name = 'mobile01'
    allowed_domains = ['www.mobile01.com']

    def __init__(self, board_f: list, max_page: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_f = board_f
        self.max_page = max_page

    def start_requests(self):
        for f in self.board_f:
            url = f'https://www.mobile01.com/topiclist.php?f={f}&p=1'
            print(url)

            yield scrapy.Request(url, meta={'now_page': 1, 'url': url})

    def parse(self, resp):
        sel = resp.css('.l-listTable')
        note_iter = sel.css('.o-fNotes::text').getall()
        for url, title, date_idx in zip(sel.css('a::attr(href)').getall(),
                                        sel.css('a::text').getall(),
                                        range(0,len(note_iter), 2)
                                        ):
            url = 'https://www.mobile01.com/' + url
            print(url)
            yield scrapy.Request(url, meta={
                'title': title,
                'last_update_date': note_iter[date_idx+1],
                'create_date': note_iter[date_idx],
                'url': url
            }, callback=self.parse_post)

    def parse_post(self, resp):
        