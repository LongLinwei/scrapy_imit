from scrapy_imit.core.spider import Spider
from scrapy_imit.core.schedule import Schedule
from scrapy_imit.core.downloder import Downloder
from scrapy_imit.core.pipeline import Pipeline
from scrapy_imit.middleware.spider_middleware import SpiderMiddleware
from scrapy_imit.middleware.downloder_middleware import DownloderMiddleware
from scrapy_imit.http.request import Request
from scrapy_imit.item import Item
from scrapy_imit.utils.log import logger
from scrapy_imit.config.setting import *
import time
import importlib

class Engine:
    def __init__(self):
        self.spiders=self.auto_import(SPIDERS,isspider=True)
        self.schedule=Schedule()
        self.downloder=Downloder()
        self.pipeline=self.auto_import(PIPELINE)
        self.spider_middleware=self.auto_import(SPIDER_MIDDLEWARES)
        self.downloder_middleware=self.auto_import(DOWNLODER_MIDDLEWARES)
    def auto_import(self,path,isspider=False):
        if isspider:
            rs={}
        else:
            rs=[]
        for i in path:
            module=importlib.import_module(i.rsplit('.',1)[0])
            attr_class=getattr(module,i.rsplit('.',1)[-1])
            if isspider:
                rs[attr_class().name]=attr_class()
            else:
                rs.append(attr_class())
        return rs

    def start_engine(self):
        for name,spider in self.spiders.items():
            for start_request in spider.start_request():
                start_request.spider_name = name
                for spider_middleware in self.spider_middleware:
                    start_request=spider_middleware.process_request(start_request)
                self.schedule.add_request(start_request)

    def request_downloder_parse(self):
        request=self.schedule.get_request()
        for downloder_middleware in self.downloder_middleware:
            request=downloder_middleware.process_request(request)
        resp=self.downloder.get_resp(request)
        for downloder_middleware in self.downloder_middleware:
            resp=downloder_middleware.process_response(resp)
        for spider_middleware in self.spider_middleware:
            resp=spider_middleware.process_response(resp)
        spider=self.spiders[request.spider_name]
        for result in spider.parse(resp):
            if isinstance(result,Request):
                for spider_middleware in self.spider_middleware:
                    result=spider_middleware.process_request(result)
                self.schedule.add_request(result)
            elif isinstance(result,Item):
                for pipeline in self.pipeline:
                    result=pipeline.process_item(result,spider)



    def start(self):

        logger.info('爬虫开启')
        start_time = time.perf_counter()
        self.start_engine()
        while True:
            self.request_downloder_parse()
            if self.schedule.total_request==self.downloder.total_resp:
                break

        logger.info('爬虫结束，共耗时{}秒'.format(time.perf_counter()-start_time))
        logger.info(f'共发送请求数量：{self.schedule.total_request}')
        logger.info(f'请求成功数：{self.downloder.total_resp}')


