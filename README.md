# ForumSpider



## Call from CrawlerProcess

```py
from forum_spider.spiders.ptt import PttSpider
from forum_spider.spiders.dcard import DcardSpider
from forum_spider.spiders.gamer import GamerSpider
from scrapy.crawler import CrawlerProcess

proc = CrawlerProcess()
proc.crawl(GamerSpider, board_bsn=[60076], max_page=1)
proc.crawl(PttSpider, board=['Gossiping'], max_page=1)
proc.start()
```

### gamer

* board_bsn: list
* max_page: int

### ptt

* board: list
* max_page: int

### dcard

* board: list
* max_page: int

## Data Field

### Base

* title
* forum
* text
* board
* author
* url
* create_date
* last_update_date
* ws_pos
* ner

## Pipelines

* set in spiders/custom_settings.py

### Dropout

* drop article has wrong 
  * text
  * title
  * url

### CKIP

* cut / pos / ner
* output: 
  * 'ws_pos': {'article': [pair('word', 'pos'), ...], 'title': [pair('word', 'pos'), ...]}
  * 'ner': [(from_index, to_index, 'NER_Category', word), ..]

### MongoDB Settings

* DB_HOST / DB_NAME: settings.py
* DOCUMENT: spiders/custom_settings.py