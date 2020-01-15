# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
from forum_spider.items import M01Item
from forum_spider.spiders.custom_settings import combine_settings
from urllib.parse import urlencode
from forum_spider.items import M01Item


class Mobile01Spider(scrapy.Spider):
    name = 'mobile01'
    allowed_domains = ['www.mobile01.com']
    custom_settings = combine_settings('m01')

    def __init__(self, board_f: list=None, board_c: list=None, max_page: int=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_f = board_f if board_f else []
        self.board_c = board_c if board_c else []
        self.max_page = max_page

    def start_requests(self):
        url = 'https://www.mobile01.com/topiclist.php?'

        for f in self.board_f:
            yield scrapy.Request(f'{url}{urlencode(args)}',
                                 meta={'now_page': 1,
                                       'base_url': url,
                                       'args': args})
        url = 'https://www.mobile01.com/forumtopic.php?'
        for c in self.board_c:
            args = {'c': c, 'p': 1}
            print(f'{url}{urlencode(args)}')
            yield scrapy.Request(f'{url}{urlencode(args)}',
                                 meta={'now_page': 1,
                                       'base_url': url,
                                       'args': args})
    def parse(self, resp):
        meta = resp.meta
        sel = resp.css('.l-listTable')
        note_iter = resp.css('.o-fNotes::text').getall()
        for url, title, date_idx in zip(sel.css('.c-listTableTd__title>a::attr(href)').getall(),
                                        sel.css(
                                            '.c-listTableTd__title>a::text').getall(),
                                        range(0, len(note_iter), 2)
                                        ):
            item = M01Item()
            item['url'] = 'https://www.mobile01.com/' + url
            item['title'] = title
            item['last_update_date'] = datetime.strptime(note_iter[date_idx+1], '%Y-%m-%d %H:%M')
            item['create_date'] = datetime.strptime(note_iter[date_idx], '%Y-%m-%d %H:%M')
            yield scrapy.Request(item['url'], meta={'item': item,
                                                    'comment_page': 1,  # comment page count
                                                    }, callback=self.parse_post)

        # next page
        if self.max_page == -1 or resp.meta['now_page'] < self.max_page:
            meta['now_page'] += 1
            meta['args']['p'] = meta['now_page']
            url = f"{meta['base_url']}{urlencode(meta['args'])}"
            # callback crawl next article list page
            yield scrapy.Request(url, meta={'now_page': meta['now_page'],
                                            'args': meta['args'],
                                            'base_url': meta['base_url']},
                                 callback=self.parse)

    def parse_post(self, resp):
        item = resp.meta['item']
        users_info = resp.css('.c-authorInfo')
        articles = resp.css('article')
        comments = item['comments'] if 'comments' in item.keys() else []
        for user_info, article, floor in zip(users_info, articles, range(len(users_info))):
            name = user_info.css('.c-authorInfo__id>a::text').get().strip()
            if floor == 0 and 'text' not in item.keys():  # 樓主
                item['author'] = name
                item['text'] = '\n'.join(article.css('div::text').getall()).strip()
            else:  # 回覆
                comment = article.css('::text').getall()
                comment = '\n'.join(comment).strip()
                comments.append({'user': name,
                                 'text': comment
                                 })
        item['comment'] = comments
        cnt = resp.meta['comment_page']
        try:
            max_cmt_page = resp.css('.l-pagination__page')[-1].css('a::attr(data-page)').get()
        except IndexError:
            max_cmt_page = None
        if max_cmt_page and max_cmt_page != str(cnt):
            yield scrapy.Request(item['url'] + urlencode({'p': cnt+1}),
                                meta={'item': item,
                                    'comment_page': cnt+1
                                    }, callback=self.parse_post)
        else:
            item['forum'] = 'mobile01'
            item['board'] = resp.css('.c-breadCrumb__item')[1].css('a::text').get().strip()
            item['sub_board'] = resp.css('.c-breadCrumb__item')[2].css('a::text').get().strip()
            item['comment_cnt'] = len(item['comment'])
            yield item
