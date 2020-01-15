from forum_spider.spiders.ptt import PttSpider
from forum_spider.spiders.dcard import DcardSpider
from forum_spider.spiders.gamer import GamerSpider
from forum_spider.spiders.mobile01 import Mobile01Spider
from scrapy.crawler import CrawlerProcess


proc = CrawlerProcess()
# proc.crawl(GamerSpider, board_bsn=[60076], max_page=1)
# proc.crawl(PttSpider, board=['Gossiping'], max_page=1)
# proc.crawl(DcardSpider, board=['relationship'], max_page=1)
proc.crawl(Mobile01Spider, board_f=['563'], max_page=1)
proc.start()
