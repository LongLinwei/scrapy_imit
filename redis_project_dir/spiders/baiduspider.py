from scrapy_redis_imit.core.spider import Spider
from scrapy_redis_imit.http.request import Request


class BaiduSpider(Spider):
    urls = ['http://www.baidu.com'] * 3
    name = 'baidu'

    def start_request(self):
        for url in self.urls:
            yield Request(url)
    def parse(self,response):
        print(response.request.proxies)
        print(response.request.proxies['http'][7:])
