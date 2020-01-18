# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy

from forum_spider.items import PttItem
from forum_spider.spiders.custom_settings import combine_settings


class PttSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    custom_settings = combine_settings(name)

    def __init__(self, board: list, max_page: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.max_page = max_page

    def start_requests(self):
        for board in self.board:
            url = 'https://www.ptt.cc/bbs/{}/index.html'.format(board)
            yield scrapy.Request(url, cookies={'over18': '1'}, meta={'board': board, 'now_page': 1})

    def parse(self, resp):
        meta = resp.meta

        for post in resp.xpath('//div[@class="r-ent"]/div[@class="title"]/a'):
            item = PttItem()
            item['board'] = meta['board']
            item['forum'] = 'ptt'
            item['url'] = resp.urljoin(post.xpath('@href').extract()[0])
            
            yield scrapy.Request(url=item['url'],
                                 cookies={'over18': '1'},
                                 meta={'item': item},
                                 callback=self.parse_post
                                 )
        if meta['now_page'] <= self.max_page or self.max_page < 0:
            next_page = resp.xpath(
                '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
            if next_page:
                url = resp.urljoin(next_page[0].extract())
                yield scrapy.Request(url=url,
                                     cookies={'over18': '1'},
                                     callback=self.parse,
                                     meta={'board': meta['board'], 'now_page': meta['now_page'] + 1}
                                     )

    def parse_post(self, resp):
        item = resp.meta['item']
        sel = resp.xpath('//div[@id="main-content"]')

        try:
            item['title'] = resp.xpath(
                '//meta[@property="og:title"]/@content').get()
        except IndexError:
            item['title'] = ''

        try:
            item['category'] = item['title'].split(']')[0].split('[')[1]
        except:
            item['category'] = ''

        data = sel.css('.article-meta-value::text').getall()
        try:
            # [0]: author, [1]: board, [2]: title [3]: date
            item['author'] = data[0].split()[0].strip()
            item['create_date'] = datetime.strptime(
                data[3], '%a %b %d %H:%M:%S %Y')
        except:
            item['author'] = ''
            item['create_date'] = datetime.strptime(
                'Mon Jan 1 00:00:00 1980', '%a %b %d %H:%M:%S %Y')
        item['last_update_date'] = item['create_date']
        # get text
        # split: date, '※ 發信站: 批踢踢實業坊'
        date = data[3] if len(data) > 3 else 'err'
        text = ' '.join(sel.xpath('//text()').getall())
        item['text'] = text.split(date)[-1].split('※ 發信站: 批踢踢實業坊(ptt.cc), ')[0]

        # get image link
        item['img_link'] = []
        for link in sel.xpath('./a/@href').getall():
            tmp = link.split('.')[-1]  # check it is image, get data type
            if tmp in ['jpg', 'png', 'gif']:
                link.replace('https', 'http')
                item['img_link'].append(link)
            elif 'imgur' in link:
                tmp = 'http://i.imgur.com/' + link.split('/')[-1]
                tmp += '.jpg'
                item['img_link'].append(tmp)
            # get ip
        for f2 in sel.xpath('./span[@class="f2"]/text()').getall():
            if '※ 發信站: 批踢踢實業坊(ptt.cc), 來自:' in f2:
                item['author_ip'] = f2.split(':')[2]
                break
        # get comment, score
        comment = []
        for com in sel.xpath('//div[@class="push"]'):
            tag = com.css('.push-tag::text').get().strip()
            user = com.css('.push-userid::text').get().split()[0].strip()
            text = com.css('.push-content::text').get().strip(': ')
            # ip = com.css('.push-ipdatetime::text').get().strip()
            # ip = ip.split(' ')[0] if '.' in ip else ''
            comment.append({'user': user, 'tag': tag, 'text': text})
        item['comment'] = comment
        yield item
