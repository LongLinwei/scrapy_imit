from scrapy_imit.http.request import Request
from scrapy_imit.item import Item
class Spider:
    url='http://www.baidu.com'
    def start_request(self):
        return Request(self.url)

    def parse(self,response):
        yield  Item(response.data)