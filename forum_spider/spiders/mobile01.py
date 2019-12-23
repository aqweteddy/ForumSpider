# -*- coding: utf-8 -*-
import scrapy


class Mobile01Spider(scrapy.Spider):
    name = 'mobile01'
    allowed_domains = ['www.mobile01.com']
    start_urls = ['http://www.mobile01.com/']

    def parse(self, response):
        pass
