from scrapy.utils.project import get_project_settings


base_settings = get_project_settings()

ptt_settings = dict(
    CONCURRENT_REQUESTS=32,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=16,
    CONCURRENT_REQUESTS_PER_IP=16,
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_MAX_DELAY=30,
    AUTOTHROTTLE_TARGET_CONCURRENCY=6,
    COL_LOGS='logs',
    COL_NAME='article',
)

dcard_settings = dict(
    CONCURRENT_REQUESTS=4,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=2,
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_MAX_DELAY=30,
    AUTOTHROTTLE_TARGET_CONCURRENCY=1.5,
    COL_LOGS='logs',
    COL_NAME='article',
)

gamer_settings = dict(
    CONCURRENT_REQUESTS=8,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=4,
    CONCURRENT_REQUESTS_PER_IP=2,
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_TARGET_CONCURRENCY=4,
    COL_LOGS='logs',
    COL_NAME='article',
)

mobile01_settings = dict(
    CONCURRENT_REQUESTS=10,
    DOWNLOAD_DELAY=0.5,
    CONCURRENT_REQUESTS_PER_DOMAIN=4,
    CONCURRENT_REQUESTS_PER_IP=2,
    AUTOTHROTTLE_START_DELAY=0.5,
    AUTOTHROTTLE_MAX_DELAY=30,
    AUTOTHROTTLE_TARGET_CONCURRENCY=5,
    COL_LOGS='logs',
    COL_NAME='article',
)


def combine_settings(spider_name: str):
    if spider_name == 'ptt':
        return {**base_settings, **ptt_settings}
    elif spider_name == 'gamer':
        return {**base_settings, **gamer_settings}
    elif spider_name == 'dcard':
        return {**base_settings, **dcard_settings}
    elif spider_name == 'm01':
        return {**base_settings, **mobile01_settings}
