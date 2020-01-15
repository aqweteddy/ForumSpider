# -*- coding: utf-8 -*-
import scrapy
from forum_spider.items import M01Item
from forum_spider.spiders.custom_settings import combine_settings
from urllib.parse import urlencode


class Mobile01Spider(scrapy.Spider):
    name = 'mobile01'
    allowed_domains = ['www.mobile01.com']

    def __init__(self, board_f: list, max_page: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_f = board_f
        self.max_page = max_page

    def start_requests(self):
        for f in self.board_f:
            args = {'f': f, 'p': 1}
            url = 'https://www.mobile01.com/topiclist.php?'
            yield scrapy.Request(url + f'{url}{urlencode(args)}',
                                 meta={'now_page': 0, 
                                       'base_url': url, 
                                       'args': args})

    def parse(self, resp):
        meta = resp.meta
        sel = resp.css('.l-listTable')
        note_iter = sel.css('.o-fNotes::text').getall()
        for url, title, date_idx in zip(sel.css('.c-listTableTd__title>a.u-ellipsis::attr(href)').getall(),
                                        sel.css(
                                            '.c-listTableTd__title>a::text').getall(),
                                        range(0, len(note_iter), 2)
                                        ):
            url = 'https://www.mobile01.com/' + url
            # print(url)
            yield scrapy.Request(url, meta={
                'title': title,
                'last_update_date': note_iter[date_idx+1],
                'create_date': note_iter[date_idx],
                'url': url
            }, callback=self.parse_post)
        
        # next page
        if self.max_page == -1 or meta['now_page'] != self.max_page:
            meta['now_page'] += 1
            meta['args']['p'] = meta['now_page']
            url = f"{meta['base_url']}{urlencode(meta['args'])}"
            try:
                yield scrapy.Request(url, meta={'now_page': meta['now_page'], 
                                                'args': meta['args'], 
                                                'base_url': meta['base_url']})
            except:
                pass

    def parse_post(self, resp):
        meta = resp.meta
        users_info = resp.css('.c-authorInfo')
        articles = resp.css('article')
        comments = meta['comments'] if 'comments' in meta.keys() else []

        for user_info, article, floor in zip(users_info, articles, range(len(users_info))):
            name = user_info.css('.c-authorInfo__id>a::text').get().strip()
            if floor == 0 and 'text' not in meta.keys(): # 樓主
                meta['author'] = name
                meta['text'] = article.css('div::text').get().strip()
            else: # 回覆｀
                comment = article.css('::text').getall()
                comment = '\n'.join(comment).strip()
                comments.append({
                    'user': name,
                    'text': comment
                })
        

        yield scrapy.Request(url, )