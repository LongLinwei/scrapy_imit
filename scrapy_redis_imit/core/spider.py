from scrapy_redis_imit.http.request import Request
from scrapy_redis_imit.item import Item


class Spider:
    urls = []

    def start_request(self):
        for url in self.urls:
            yield Request(url)

    def parse(self, response):
        yield Item(response.text)


class ProxiSpdider(Spider):
    urls = []
    name = ''
    list_pattern = ''
    host_pattern = ''
    port_pattern = ''

    def parse(self, response):
        tr_list = response.xpath(self.list_pattern)[1:]
        # print(tr_list)
        if tr_list:
            for tr in tr_list:
                host = tr.xpath(self.host_pattern)[0].strip()
                port = tr.xpath(self.port_pattern)[0].strip()
                proxy = f"{host}:{port}"
                yield Item(proxy)


class GenneralSpdider(Spider):
    urls = []
    name = ''
    list_pattern = ''
    target_pattern = ''

    def parse(self, response):
        tr_list = response.xpath(self.list_pattern)
        # print(tr_list)
        if tr_list:
            for tr in tr_list:
                target = tr.xpath(self.target_pattern)[0].strip()

                yield Item(target)
