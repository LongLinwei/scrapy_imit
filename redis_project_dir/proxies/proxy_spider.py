from scrapy_redis_imit.core.spider import ProxiSpdider,GenneralSpdider
from scrapy_redis_imit.item import Item

class ProxySpider(ProxiSpdider):
    urls = [f'https://www.xicidaili.com/nn/{i}'.format(i) for i in range(41,2000)]
    name = 'proxy'
    list_pattern = '//table[@id="ip_list"]//tr[@class="odd"]'
    host_pattern = './/td[2]/text()'
    port_pattern = './/td[3]/text()'

class KuaiSpider(ProxiSpdider):
    urls=[f'https://www.kuaidaili.com/free/inha/{i}/' for i in range(41,2000)]+[f'https://www.kuaidaili.com/free/intr/{i}/' for i in range(21,40)]
    name='kuai'
    list_pattern = '//tbody/tr'
    host_pattern = './/td[@data-title="IP"]/text()'
    port_pattern = './/td[@data-title="PORT"]/text()'

class EightSpider(ProxiSpdider):
    urls=[f'http://www.89ip.cn/index_{i}.html/' for i in range(1,40)]
    name='eight'
    list_pattern = '//table[@class="layui-table"]/tbody/tr'
    host_pattern = './/td[1]/text()'
    port_pattern = './/td[2]/text()'
class IphaiSpider(ProxiSpdider):
    urls=['http://www.iphai.com/free/ng']
    name='iphai'
    list_pattern = '//table/tr'
    host_pattern = './/td[1]/text()'
    port_pattern = './/td[2]/text()'
class XilaSpider(GenneralSpdider):
    urls=[f'http://www.xiladaili.com/gaoni/{i}/' for i in range(199,200)]
    name='xila'
    list_pattern = '//tbody/tr'
    target_pattern  = './/td[1]/text()'
class NimaSpider(GenneralSpdider):
    urls=[f'http://www.nimadaili.com/gaoni/{i}/' for i in range(995,1000)]
    name='nima'
    list_pattern = '//tbody/tr'
    target_pattern  = './/td[1]/text()'


