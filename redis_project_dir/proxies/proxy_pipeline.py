from scrapy_redis_imit.core.pipeline import Pipeline
from scrapy_redis_imit.utils.proxies_db import ProxiesDb
class ProxyPipeline(Pipeline):
    def __init__(self):
        self.proxies_db=ProxiesDb()
    def process_item(self, item,spider):
        # if spider.name=='proxy':
        print(item.data)
        self.proxies_db.add(item.data)
        # return item