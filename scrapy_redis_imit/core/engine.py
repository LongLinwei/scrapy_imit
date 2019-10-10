from scrapy_redis_imit.core.spider import Spider
from scrapy_redis_imit.core.schedule import Schedule
from scrapy_redis_imit.core.downloder import Downloder
from scrapy_redis_imit.core.pipeline import Pipeline
from scrapy_redis_imit.middleware.spider_middleware import SpiderMiddleware
from scrapy_redis_imit.middleware.downloder_middleware import DownloderMiddleware
from scrapy_redis_imit.utils.count import Count
from scrapy_redis_imit.http.request import Request
from scrapy_redis_imit.item import Item
from scrapy_redis_imit.utils.log import logger
from scrapy_redis_imit.config.setting import *
import time
import importlib
from multiprocessing.dummy import Pool


class Engine:
    def __init__(self):
        self.count = Count()
        self.spiders = self.auto_import(SPIDERS, isspider=True)
        self.schedule = Schedule(self.count)
        self.downloder = Downloder()
        self.pipeline = self.auto_import(PIPELINE)
        self.spider_middleware = self.auto_import(SPIDER_MIDDLEWARES)
        self.downloder_middleware = self.auto_import(DOWNLODER_MIDDLEWARES)
        self.pool = Pool(PROCESSING_NUM)
        self.stop_flag = False


    def auto_import(self, path, isspider=False):
        if isspider:
            rs = {}
        else:
            rs = []
        for i in path:
            module = importlib.import_module(i.rsplit('.', 1)[0])
            attr_class = getattr(module, i.rsplit('.', 1)[-1])
            if isspider:
                rs[attr_class().name] = attr_class()
            else:
                rs.append(attr_class())
        return rs

    def start_engine(self):
        def start_first_request(name,spider):
            for start_request in spider.start_request():
                start_request.spider_name = name
                for spider_middleware in self.spider_middleware:
                    start_request = spider_middleware.process_request(start_request)
                self.schedule.add_request(start_request)
            self.count.incr_start_spider_num()
        for name, spider in self.spiders.items():
            self.pool.apply_async(start_first_request,args=(name,spider))

    def request_downloder_parse(self):
        request = self.schedule.get_request()
        if not request:
            return
        for downloder_middleware in self.downloder_middleware:
            request = downloder_middleware.process_request(request)
        resp = self.downloder.get_resp(request)
        resp.meta = request.meta
        for downloder_middleware in self.downloder_middleware:
            resp = downloder_middleware.process_response(resp)
        for spider_middleware in self.spider_middleware:
            resp = spider_middleware.process_response(resp)
        spider = self.spiders[request.spider_name]
        parse = getattr(spider, request.callback)
        for result in parse(resp):
            if isinstance(result, Request):
                result.spider_name = spider.name
                for spider_middleware in self.spider_middleware:
                    result = spider_middleware.process_request(result)
                self.schedule.add_request(result)
            elif isinstance(result, Item):
                for pipeline in self.pipeline:
                    result = pipeline.process_item(result, spider)
        # self.downloder.total_resp += 1
        self.count.incr_total_resp()
        # print(self.schedule.total_repeat_request,self.schedule.total_request,self.downloder.total_resp)

    def _backfun(self, temp):
        if not self.stop_flag:
            self.pool.apply_async(self.request_downloder_parse, callback=self._backfun)

    def start(self):

        logger.info('爬虫开启')
        start_time = time.perf_counter()
        if OPEN_PROCESSING:
            self.pool.apply_async(self.start_engine)
            for i in range(PROCESSING_NUM):
                self.pool.apply_async(self.request_downloder_parse, callback=self._backfun)
        else:
            self.start_engine()
        while True:
            if OPEN_PROCESSING:
                time.sleep(0.001)
            else:
                self.request_downloder_parse()
            # if self.schedule.total_request != 0:
            #     if self.schedule.total_request == self.downloder.total_resp + self.schedule.total_repeat_request:
            if self.count.start_spider_num== len(self.spiders):
                if self.count.total_request == self.count.total_resp + self.count.total_repeat_request:
                    self.stop_flag = True
                    break

        logger.info('爬虫结束，共耗时{}秒'.format(time.perf_counter() - start_time))
        # logger.info(f'共发送请求数量：{self.schedule.total_request}')
        # logger.info(f'请求成功数：{self.downloder.total_resp}')
        # logger.info(f'重复请求{self.schedule.total_repeat_request}')
        logger.info(f'共发送请求数量：{self.count.total_request}')
        logger.info(f'请求成功数：{self.count.total_resp}')
        logger.info(f'重复请求{self.count.total_repeat_request}')
        self.count.clear()
        self.schedule.ins_list.clear()
