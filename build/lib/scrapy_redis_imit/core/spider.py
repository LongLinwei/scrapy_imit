from scrapy_redis_imit.http.request import Request
from scrapy_redis_imit.item import Item


class Spider:
    url = 'http://www.baidu.com'

    def start_request(self):
        yield Request(self.url)

    def parse(self, response):
        yield Item(response.text)
