from scrapy_imit.core.spider import Spider
from scrapy_imit.http.request import Request


class BaiduSpider(Spider):
    urls = ['http://www.baidu.com'] * 3
    name = 'baidu'

    def start_request(self):
        for url in self.urls:
            yield Request(url)
