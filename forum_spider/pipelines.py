# -*- coding: utf-8 -*-
from datetime import datetime

from ckiptagger import NER, POS, WS
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

# TODO: Pipline: DB Pipeline
# * Done: MongoDB
# TODO: Process Item Pipeline(cut / NER ...)


class CkipPipeline:
    def open_spider(self, spider):
        self.ws = WS('./ckip_model', disable_cuda=False)
        self.pos = POS('./ckip_model', disable_cuda=False)
        self.ner = NER('./ckip_model', disable_cuda=False)

    def process_item(self, item, spider):
        if not item['title'] or not item['text']:
            return
        title_seg, article_seg = self.ws([item['title'],
                                          item['text']])
        title_pos, article_pos = self.pos([title_seg, article_seg])
        title_ner, article_ner = self.ner(
            [title_seg, article_seg], [title_pos, article_pos])

        item['ws_pos'] = {'title': map(self.make_pair, title_seg, title_pos),
                          'text': map(self.make_pair, article_seg, article_pos)}

        item['ner'] = {'title': title_ner, 'text': article_ner}
        return item

    @staticmethod
    def make_pair(x, y): return [x, y]


# MongoDB pipeline


class MongoDbPipeline:
    def open_spider(self, spider):
        settings = get_project_settings()
        cli = MongoClient(settings['MONGO_HOST'])
        self.cur = cli[settings['MONGO_DB']
                       ][spider.custom_settings['COL_NAME']]
        self.cur_logs = cli[settings['MONGO_DB']
                            ][spider.custom_settings['COL_LOGS']]
        self.start_time = datetime.now()

    def process_item(self, item, spider):
        print(item['url'])
        self.cur.update_one({'url': item['url']}, {
                            '$set': dict(item)}, upsert=True)
        yield item

    def close_spider(self, spider):
        end_time = datetime.now()
        val = {
            'spider_name': spider.name,
            'start_time': self.start_time,
            'end_time': end_time,
        }
        self.cur_logs.insert(val)
