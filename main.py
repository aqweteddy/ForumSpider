import time
from argparse import ArgumentParser

from forum_spider.spiders.ptt import PttSpider
from forum_spider.spiders.dcard import DcardSpider
from forum_spider.spiders.gamer import GamerSpider
from forum_spider.spiders.mobile01 import Mobile01Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

start = time.time()
parser = ArgumentParser()
parser.add_argument('--ptt_page', type=int, default=1, help='ptt spider pages for each board')
parser.add_argument('--dcard_page', type=int, default=1, help='dcard spider pages for each board')
parser.add_argument('--gamer_page', type=int, default=1, help='gamer spider pages for each board')
parser.add_argument('--m01_page', type=int, default=1, help='mobile01 spider pages for each board')

args = parser.parse_args()
# 政治 廢文 3C 閒聊 生活 汽機車 感情 股票 電玩
PTT_BOARD = ['Gossiping', 'C_Chat', 'NBA', 'HatePolitics', 'Lifeismoney', 'Stock', 'Baseball', 'sex','movie', 'WomenTalk', 'car', 'Beauty', 'MobileComm', 'Boy-Girl', 'marriage', 'joke', 'StupidClown']
# PTT_BOARD = ['C_Chat']
DCARD_BOARD = ['hot']
# 場外、講談說論、Joke
GAMER_BOARD = [60076, 60440, 60555, 60030] 
# GAMER_BOARD = [60076]
# 手機 相機 筆電 電腦 蘋果 影音 汽車 機車 單車 遊戲 居家 女性 時尚 運動 戶外 生活 旅遊 閒聊 時事
MOB01_BOARD_C = [16, 20, 19, 17, 30, 28, 21, 29, 24, 23, 26, 27, 31, 33, 3, 35, 18, 36]
# MOB01_BOARD_C = [16, 20]
proc = CrawlerProcess(get_project_settings())
proc.crawl(GamerSpider, board_bsn=GAMER_BOARD, max_page=args.gamer_page)
proc.crawl(PttSpider, board=PTT_BOARD, max_page=args.ptt_page)
proc.crawl(DcardSpider, board=DCARD_BOARD, max_page=args.dcard_page)
proc.crawl(Mobile01Spider, board_c=MOB01_BOARD_C, max_page=args.m01_page)
proc.start()

print(f'Total Time: {time.time() - start} sec')
