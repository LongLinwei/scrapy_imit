from scrapy_imit.core.spider import Spider
from scrapy_imit.http.request import Request
from scrapy_imit.item import Item
from copy import deepcopy
class GuokeSpider(Spider):
    urls=['https://www.guokr.com/ask/newest/']
    name='guoke'
    def start_request(self):
        for url in self.urls:
            yield Request(url)
    def parse(self,response):
        item={}
        li_lst=response.xpath('//ul[@class="ask-list"]/li')
        for li in li_lst:
            item['title']=li.xpath('.//h2//text()')[0].strip()
            item['href']=li.xpath('.//h2/a/@href')[0]
            yield Request(item['href'],callback='parse_detail',meta=deepcopy(item))
    def parse_detail(self,response):
        item=response.meta
        item['focus_num']=response.xpath('//span[@id="followNum"]/text()')
        yield Item(item)
