from scrapy_redis_imit.core.spider import Spider
from scrapy_redis_imit.http.request import Request
import time
class XinlangSpider(Spider):
    urls = ['https://hq.sinajs.cn/?rn=1570690553263&list=sz300136,sz002600,sz002714,sz300601,sz300433,sh603927,sz002241,sz300379,sz000063,sz300729,sh603933,sh603927,sz300790,sz300772,sh603681,sh603121,sz002962,sz002961,sz002415,sh603927,sz000725,sz002463,sz002230,sz002600,sz002236,sz300014,sh600519,sz300136']
    name = 'xinlang'

    def start_request(self):
        while True:
            for url in self.urls:
                yield Request(url,filter=False)
            print('='*100)
            time.sleep(10)
