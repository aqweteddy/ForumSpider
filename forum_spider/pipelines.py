# -*- coding: utf-8 -*-
from datetime import datetime

from ckiptagger import NER, POS, WS
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem

# TODO: Pipeline LOGS
# TODO: export to json / csv
# * Done: MongoDB
# * Done: Process Item Pipeline(cut / NER ...)


class DropoutPipeline:
    def process_item(self, item, spider):
        if not item.get('title', '') or not item.get('text', '') or not item.get('url', ''):
            raise DropItem("Drop article")
        return item


class CkipPipeline:
    def open_spider(self, spider):
        spider.log('CkipPipeline: Init model...')
        self.ws = WS('./ckip_model', disable_cuda=False)
        self.pos = POS('./ckip_model', disable_cuda=False)
        self.ner = NER('./ckip_model', disable_cuda=False)
        self.cnt = 0

    def process_item(self, item, spider):
        self.cnt += 1
        if self.cnt % 100 == 0:
            spider.log(f'CkipPipeline: {self.cnt}, {item["title"]}')
        title_seg, article_seg = self.ws([item['title'],
                                          item['text']])
        title_pos, article_pos = self.pos([title_seg, article_seg])
        title_ner, article_ner = self.ner(
            [title_seg, article_seg], [title_pos, article_pos])

        item['ws_pos'] = {'title': list(map(self.make_pair, title_seg, title_pos)),
                          'text': list(map(self.make_pair, article_seg, article_pos))}

        title_ner = [(a, b, cat, word) for a, b, cat, word in title_ner if cat not in [
            'ORDINAL', 'CARDINAL', 'DATE', 'ORDINAL', 'QUANTITY', 'PERCENT', 'TIME']]
        article_ner = [(a, b, cat, word) for a, b, cat, word in article_ner if cat not in [
            'ORDINAL', 'CARDINAL', 'DATE', 'ORDINAL', 'QUANTITY', 'PERCENT', 'TIME']]
        item['ner'] = {'title': list(title_ner), 'text': list(article_ner)}
        return item

    @staticmethod
    def make_pair(x, y): return [x, y]


class MongoDbPipeline:
    def open_spider(self, spider):
        spider.log('MongoDbPipeline: connect to db')
        settings = get_project_settings()
        cli = MongoClient(settings['MONGO_HOST'])
        self.cur = cli[settings['MONGO_DB']
                       ][spider.custom_settings['COL_NAME']]
        self.cur_logs = cli[settings['MONGO_DB']
                            ][spider.custom_settings['COL_LOGS']]
        self.start_time = datetime.now()

    def process_item(self, item, spider):

        self.cur.update_one({'url': item['url']}, {
                            '$set': dict(item)}, upsert=True)
        return item

    def close_spider(self, spider):
        end_time = datetime.now()
        val = {
            'spider_name': spider.name,
            'start_time': self.start_time,
            'end_time': end_time,
        }
        self.cur_logs.insert(val)
