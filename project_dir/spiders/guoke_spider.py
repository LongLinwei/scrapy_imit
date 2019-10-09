from scrapy_imit.core.spider import Spider
from scrapy_imit.http.request import Request
class GuokeSpider(Spider):
    urls=['https://www.guokr.com/ask/newest/']
    name='guoke'
    def start_request(self):
        for url in self.urls:
            yield Request(url)