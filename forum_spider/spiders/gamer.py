# -*- coding: utf-8 -*-
import scrapy

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
            url = 'https://forum.gamer.com.tw/B.php?bsn={}'.format(bsn)
            yield scrapy.Request(url=url, callback=self.parse, meta={
                'page': 1,
                'bsn': bsn
            })

    def parse(self, resp):

        for sel in resp.css('.b-list-item'):
            item = GamerItem()
            item['forum'] = 'gamer'
            try:
                item['url'] = 'https://forum.gamer.com.tw/' + \
                    sel.css('.b-list__main>a::attr(href)').get()
                item['author'] = sel.css('.b-list__count__user>a::text').get()
                item['board_bsn'] = resp.meta['bsn']
                yield scrapy.Request(url=item['url'],
                                     callback=self.parse_post,
                                     meta={'item': item}
                                     )
            except TypeError:
                pass

        if resp.meta['page'] < self.max_page:
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
            if sel.css('.c-post__header__title'):
                item['title'] = sel.css('.c-post__header__title::text').get()
                item['last_update_date'] = ' '.join(sel.css('.edittime::text').get().split()[:-2])
                item['text'] = ''.join(
                    sel.css('.c-article__content *::text').getall())
                item['reply'] = {
                    'text': sel.css('.reply-content__article *::text').getall(),
                    'author': sel.css('.reply-content__user *::text').getall()
                }
            elif sel.css('.c-article__content *::text'):
                # comment
                comment.append({
                    'text': ''.join(sel.css('.c-article__content *::text').getall()),
                    'author': sel.css('.c-user__avatar::attr(data-gamercard-userid)').get(),
                    'last_update_date': sel.css('.edittime::text').get(),
                    'reply': {
                        'text': sel.css('.reply-content__article *::text').getall(),
                        'author': sel.css('.reply-content__user *::text').getall()
                    }
                })
            item['comment'] = comment
            yield item
