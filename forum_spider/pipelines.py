# -*- coding: utf-8 -*-
from datetime import datetime
import json, re

from ckiptagger import NER, POS, WS
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from gaisTokenizer import Tokenizer
# import gaipy as gp

# TODO: Pipeline LOGS
# TODO: export to json / csv
# FIXME: NuDB Pipeline
# * Done: MongoDB
# * Done: Process Item Pipeline(cut / NER ...)


class DropoutPipeline:
    def open_spider(self, spider):
        self.cnt = 0  # number of DropItem

    def process_item(self, item, spider):
        if not item.get('title', None):
            self.cnt += 1
            raise DropItem("Drop article because of title")
        if not item.get('text', None):
            self.cnt += 1
            raise DropItem("Drop article because of text")
        if not item.get('url', None):
            self.cnt += 1
            raise DropItem("Drop article because of url")
        return item

    def close_spider(self, spider):
        print(f'Drop {self.cnt} items.')


class TextPreprocessPipeline:
    DISABLE_CUDA = True
    TOKEN = 'pX5C62575A587D56505F65505E5C7D5D5F3A193206221B30532B25030F382231021D2417063B1E5336071F145B52A9FAEB8BC1E48CD6EB5DFN'

    def open_spider(self, spider):
        settings = get_project_settings()
        cli = MongoClient(settings['MONGO_HOST'])
        self.cur = cli[settings['MONGO_DB']
                       ][spider.custom_settings['COL_NAME']]
        

        self.tokenizer = Tokenizer(self.TOKEN)

        # self.ws = WS('./ckip_model', disable_cuda=self.DISABLE_CUDA)
        self.pos = POS('./ckip_model', disable_cuda=self.DISABLE_CUDA)
        self.ner = NER('./ckip_model', disable_cuda=self.DISABLE_CUDA)

    def __remove_special_chars(self, text: str):
        # remove url
        text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", text)
        # remove sent from ... 
        text = text.split('--\nSent ')[0]
        # keep only eng, zh, number
        rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
        text = rule.sub(' ', text)
        # remove space
        text = ' '.join(text.split())
        return text


    def process_item(self, item, spider):
        item['raw_title'] = self.__remove_special_chars(item['title'])
        item['raw_text'] = self.__remove_special_chars(item['text'])
        
        if self.cur.find_one({'url': item['url'], 'last_update_date': item['last_update_date']}):
            spider.logger.debug(f"already existed {item['url']}")
            return item
        
        # GAIS Tokenize
        item['text_seg'] = self.tokenizer.tokenize(item['raw_text'])
        item['title_seg'] = self.tokenizer.tokenize(item['raw_title'])

        # item['text_seg'], item['title_seg'] = self.ws(
        #     [item['text'], item['title']])
        item['text_pos'], item['title_pos'] = self.pos(
            [item['text_seg'], item['title_seg']])
        item['text_ner'], item['title_ner'] = self.ner([item['text_seg'], item['title_seg']],
                                                       [item['text_pos'],
                                                           item['title_pos']]
                                                       )
        def ner_filter(cat): return True if cat not in [
            'ORDINAL', 'CARDINAL', 'DATE', 'ORDINAL', 'QUANTITY', 'PERCENT', 'TIME'] else False

        item['title_ner'] = [(a, b, cat, word) for a, b,
                             cat, word in item['title_ner'] if ner_filter(cat)]
        item['text_ner'] = [(a, b, cat, word) for a, b, cat,
                            word in item['text_ner'] if ner_filter(cat)]

        return item


class GaisDbPipeline:
    def open_spider(self, spider):
        print(f'gaisdb Pipeline load')
        self.db_name = 'forum_spider'
        self.db_args = {'title': 'text',
                        'text': 'text',
                        'forum': 'text',
                        'board': 'text',
                        'author': 'text',
                        'url': 'text',
                        'comment_cnt': 'num',
                        'create_date': 'date',
                        'last_update_date': 'date',
                        'comment': 'text'
                        }

    def process_item(self, item, spider):
        item['comment'] = str(item['comment'])
        url = urlencode(item['url'])
        ret_sel = gp.Select(
            self.db_name, {'col': ['url'], 'val': [url]})
        ret_sel = json.loads(ret_sel, encoding='utf-8')['data']
        ret_sel = json.loads(ret_sel, encoding='utf-8')
        item = dict(item)
        if ret_sel['cnt'] > 0:
            rec_id = ret_sel['recs'][0]['_rid']
            resp = gp.Update(self.db_name, rec_id, item,
                             modify_all=True, record_format='json')

        else:
            resp = gp.Insert(self.db_name, item, record_format='json')
        

class MongoDbPipeline:
    def open_spider(self, spider):
        spider.logger.info(f'spider: {spider.name}')
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
        spider.logger.info(f'{spider.name} finished')
        self.cur_logs.insert(val)
