# -*- coding: utf-8 -*-
from datetime import datetime

from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

# TODO: Pipline: DB Pipeline 
# *Done: MongoDB
# TODO: Process Item Pipeline(cut / NER ...)



# MongoDB pipeline
class MongoDbPipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        cli = MongoClient(settings['MONGO_HOST'])
        self.cur = cli[settings['MONGO_DB']][spider.custom_settings['COL_NAME']]
        self.cur_logs = cli[settings['MONGO_DB']][spider.custom_settings['COL_LOGS']]
        self.start_time = datetime.now()

    def process_item(self, item, spider):
        print(item['url'])
        self.cur.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
    
    def close_spider(self, spider):
        end_time = datetime.now()
        val = {
            'spider_name': spider.name,
            'start_time': self.start_time,
            'end_time': end_time,
        }
        self.cur_logs.insert(val)