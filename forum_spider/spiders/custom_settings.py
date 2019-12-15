from scrapy.utils.project import get_project_settings

base_settings = get_project_settings()

ptt_settings = dict(
    CONCURRENT_REQUESTS=32,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=16,
    CONCURRENT_REQUESTS_PER_IP=16,
    USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
               ' Safari/537.36',
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_MAX_DELAY=30,
    AUTOTHROTTLE_TARGET_CONCURRENCY=5,
    COL_LOGS='logs',
    COL_NAME='article',
    ITEM_PIPELINES={
        'forum_spider.pipelines.DropoutPipeline': 100,
        'forum_spider.pipelines.CkipPipeline': 200,
        'forum_spider.pipelines.MongoDbPipeline': 300
    }
)

dcard_settings = dict(
    CONCURRENT_REQUESTS=2,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=2,
    CONCURRENT_REQUESTS_PER_IP=2,
    USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
               ' Safari/537.36',
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_MAX_DELAY=30,
    AUTOTHROTTLE_TARGET_CONCURRENCY=2,
    COL_LOGS='logs',
    COL_NAME='article',
    ITEM_PIPELINES={
        'forum_spider.pipelines.MongoDbPipeline': 300,
    }
)

gamer_settings = dict(
    CONCURRENT_REQUESTS=4,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=4,
    CONCURRENT_REQUESTS_PER_IP=2,
    USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87'
               ' Safari/537.36',
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_MAX_DELAY=30,
    AUTOTHROTTLE_TARGET_CONCURRENCY=2,
    COL_LOGS='logs',
    COL_NAME='article',
    ITEM_PIPELINES={
        'forum_spider.pipelines.MongoDbPipeline': 300,
    }
)

def combine_settings(spider_name: str):
    if spider_name == 'ptt':
        return {**base_settings, **ptt_settings}
    elif spider_name == 'gamer':
        return {**base_settings, **gamer_settings}
    elif spider_name == 'dcard':
        return {**base_settings, **dcard_settings}
