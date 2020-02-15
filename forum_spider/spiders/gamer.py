# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from forum_spider.items import GamerItem
from forum_spider.spiders.custom_settings import combine_settings


class GamerSpider(scrapy.Spider):
    name = 'gamer'
    allowed_domains = ['forum.gamer.com.tw']
    custom_settings = combine_settings(name)

    def __init__(self, board_bsn: list, max_page: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bsn = board_bsn
        self.max_page = max_page

    def start_requests(self):
        for bsn in self.bsn:
            self.logger.info(f'Now bsn: {bsn}')
            url = 'https://forum.gamer.com.tw/B.php?bsn={}'.format(bsn)
            yield scrapy.Request(url=url, callback=self.parse, meta={
                'page': 1,
                'bsn': bsn
            })

    def parse(self, resp):
        meta = resp.meta
        self.logger.info(f'bsn: {meta["bsn"]} Page: {meta["page"]}')

        for sel in resp.css('.b-list-item'):
            item = GamerItem()
            item['forum'] = 'gamer'
            try:
                item['url'] = 'https://forum.gamer.com.tw/' + \
                    sel.css('.b-list__main>a::attr(href)').get()
                item['board_bsn'] = resp.meta['bsn']
                yield scrapy.Request(url=item['url'],
                                     callback=self.parse_post,
                                     meta={'item': item}
                                     )
            except TypeError:
                pass

        if resp.meta['page'] < self.max_page and resp.meta['page'] < 100:
            url = resp.css('.next::attr(href)').get()
            if url:
                yield scrapy.Request(url='https://forum.gamer.com.tw/B.php' + url,
                                     callback=self.parse,
                                     meta={'page': resp.meta['page'] + 1}
                                     )

    def parse_post(self, resp):
        item = resp.meta['item']
        comment = []
        for sel in resp.css('.c-section'):
            # article
            if sel.css('.c-post__header__title'):  # text
                item['title'] = sel.css(
                    '.c-post__header__title::text').get().strip()
                item['author'] = sel.css(
                    '.c-post__header__author>a.username::text').get().strip()
                item['text'] = ''.join(
                    sel.css('div.c-article__content ::text').getall()).strip()
                item['text'] += '\n'.join(
                    sel.css('div.c-article__content ::attr(href)').getall()).strip()
                item['create_date'] = sel.css(
                    'a.edittime::attr(data-mtime)').get().strip()
                item['last_update_date'] = datetime.strptime(
                    item['create_date'], '%Y-%m-%d %H:%M:%S')
                item['create_date'] = item['last_update_date']
                tmp = sel.css('a.count::text').getall()
                item['like_cnt'] = 0 if tmp[0] == '-' else int(tmp[0]) if tmp[0] != '爆' else 1000
                item['dislike_cnt'] = 0 if tmp[1] == '-' else int(tmp[1]) if tmp[1] != 'X' else 1000
            if sel.css('.c-article__content *::text') and not sel.css('.c-post__header__title'):
                # comment
                comment.append({
                    'author': sel.css('.c-post__header__author>a.username::text').get().strip(),
                    'text': ''.join(sel.css('div.c-article__content ::text').getall()).strip()
                })
                # short reply
                for author, text in zip(sel.css('.reply-content__user ::text').getall(),
                                        sel.css('.reply-content__article ::text').getall()):
                    comment.append({
                        'author': author.strip(),
                        'text': text.strip()
                    })

        item['comment'] = comment

        yield item
