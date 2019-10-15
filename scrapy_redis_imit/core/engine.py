from scrapy_redis_imit.core.spider import Spider
from scrapy_redis_imit.core.schedule import Schedule
from scrapy_redis_imit.core.downloder import Downloder
from scrapy_redis_imit.core.pipeline import Pipeline
from scrapy_redis_imit.middleware.spider_middleware import SpiderMiddleware
from scrapy_redis_imit.middleware.downloder_middleware import DownloderMiddleware
from scrapy_redis_imit.utils.count import Count
from scrapy_redis_imit.utils.proxies_db import ProxiesDb
from scrapy_redis_imit.utils.aio_proxies_db import  AioProxiesDb
from scrapy_redis_imit.http.request import Request
from scrapy_redis_imit.item import Item
from scrapy_redis_imit.utils.log import logger
from scrapy_redis_imit.utils.queue import BackupQueue
from scrapy_redis_imit.config.setting import *
import time
import importlib
import requests
from multiprocessing.dummy import Pool
from urllib3 import exceptions
import aiohttp
import asyncio
# from aiomultiprocess import Pool as AioPool

class Engine:
    def __init__(self):
        self.count = Count()
        self.backupqueue = BackupQueue()
        self.proxies_db = ProxiesDb()
        self.spiders = self.auto_import(SPIDERS, isspider=True)
        self.schedule = Schedule(self.count)
        self.downloder = Downloder(self.count, self.backupqueue, self.proxies_db)
        self.pipeline = self.auto_import(PIPELINE)
        self.spider_middleware = self.auto_import(SPIDER_MIDDLEWARES)
        self.downloder_middleware = self.auto_import(DOWNLODER_MIDDLEWARES)
        self.pool = Pool(PROCESSING_NUM)
        self.stop_flag = False
        self.aio_proxies_db=AioProxiesDb()

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
        def start_first_request(name, spider):
            for start_request in spider.start_request():
                start_request.spider_name = name
                for spider_middleware in self.spider_middleware:
                    start_request = spider_middleware.process_request(start_request)
                self.schedule.add_request(start_request)
            self.count.incr_start_spider_num()

        for name, spider in self.spiders.items():
            self.pool.apply_async(start_first_request, args=(name, spider))

    def request_downloder_parse(self):
        request = self.schedule.get_request()
        if not request:
            return
        self.backupqueue.put(request)
        if USE_PROXY:
            proxy = self.proxies_db.get().decode()
            print(self.proxies_db.score(proxy))
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            request.proxies = proxies
        for downloder_middleware in self.downloder_middleware:
            request = downloder_middleware.process_request(request)
        resp = self.downloder.get_resp(request)
        if not resp:
            return
        resp.meta = request.meta
        for downloder_middleware in self.downloder_middleware:
            resp = downloder_middleware.process_response(resp)
        for spider_middleware in self.spider_middleware:
            resp = spider_middleware.process_response(resp)
        spider = self.spiders[request.spider_name]
        parse = getattr(spider, request.callback)
        results = parse(resp)
        if results:
            for result in results:
                # logger.info(result)
                if isinstance(result, Request):
                    result.spider_name = spider.name
                    for spider_middleware in self.spider_middleware:
                        result = spider_middleware.process_request(result)
                    self.schedule.add_request(result)
                elif isinstance(result, Item):
                    for pipeline in self.pipeline:
                        result = pipeline.process_item(result, spider)
        # self.downloder.total_resp += 1
        self.backupqueue.pop()
        self.count.incr_total_resp()
        logger.info(f"成功处理完成 {request.url}")
        # print(self.schedule.total_repeat_request,self.schedule.total_request,self.downloder.total_resp)

    def _backfun(self, temp):
        if not self.stop_flag:
            self.pool.apply_async(self.request_downloder_parse, callback=self._backfun)

    def start_spider(self):

        logger.info('爬虫开启')
        start_time = time.perf_counter()
        while self.backupqueue.llen():
            self.backupqueue.rpoplpush()
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
            if self.count.start_spider_num >= len(self.spiders):
                if self.count.total_request == self.count.total_resp + self.count.total_repeat_request + self.count.fail_request_num:
                    self.stop_flag = True
                    break

        logger.info('爬虫结束，共耗时{}秒'.format(time.perf_counter() - start_time))
        # logger.info(f'共发送请求数量：{self.schedule.total_request}')
        # logger.info(f'请求成功数：{self.downloder.total_resp}')
        # logger.info(f'重复请求{self.schedule.total_repeat_request}')
        logger.info(f'共发送请求数量：{self.count.total_request}')
        logger.info(f'请求成功数：{self.count.total_resp}')
        logger.info(f'重复请求：{self.count.total_repeat_request}')
        logger.info(f'请求失败：{self.count.fail_request_num}')
        self.count.clear()
        self.schedule.ins_list.clear()
    def request_except_process(self,fun):
        def inner(*args):
            resp=None
            try:
                fun()
            except ConnectionRefusedError:
                logger.info('拒绝连接')
            except exceptions.ConnectTimeoutError:
                logger.info('连接超时')
            except exceptions.MaxRetryError:
                logger.info('超过最大尝试次数')
            except requests.exceptions.ProxyError:
                logger.info('代理错误，目标计算机积极拒绝')
            except requests.exceptions.ConnectTimeout:
                logger.info('连接超时')
            except Exception as e:
                logger.info(e)
            finally:
                self.proxies_db.decr(args[0])
            return resp
        return inner


    def start_proxy_ready(self):
        proxy =self.proxies_db.first_get()
        # print(self.proxies_db.score(proxy))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        # print(proxies)
        # exit()
        # resp = None
        # try:
        #     resp = requests.get(READY_URL, headers=headers, proxies=proxies, timeout=5)
        # except ConnectionRefusedError:
        #     logger.info('拒绝连接')
        # except exceptions.ConnectTimeoutError:
        #     logger.info('连接超时')
        # except exceptions.MaxRetryError:
        #     logger.info('超过最大尝试次数')
        # except requests.exceptions.ProxyError:
        #     logger.info('代理错误，目标计算机积极拒绝')
        # except requests.exceptions.ConnectTimeout:
        #     logger.info('连接超时')
        # except Exception as e:
        #     logger.info(e)
        # finally:
        #     self.proxies_db.decr(proxy)

        @self.request_except_process
        def get_requests(*args):
            resp= requests.get(READY_URL, headers=headers, proxies=args[1], timeout=5)
        resp=get_requests(proxy,proxies)
        if not resp:
            return
        if resp.status_code == 200:
            self.proxies_db.set_max(proxy)
        else:
            self.proxies_db.decr(proxy)

    def start_proxies_ready(self):
        for i in range(PROCESSING_NUM):
            self.pool.apply_async(self.start_proxy_ready, callback=self.proxies_callback)
        while not self.stop_flag:
            time.sleep(1)
            if not self.proxies_db.count():
                self.stop_flag = True

    def proxies_callback(self, temp):
        if not self.stop_flag:
            self.pool.apply_async(self.start_proxy_ready, callback=self.proxies_callback)
    async def get_resp(self,headers):
        # await asyncio.sleep(0.1)
        proxy=await self.aio_proxies_db.first_get()
        # print(1)
        proxy=proxy.decode()
        proxies='http://'+proxy
        resp=None
        try:
            resp=await self.session.head(READY_URL,proxy=proxies,headers=headers)
        except ConnectionRefusedError:
            logger.info('拒绝连接')
        except exceptions.ConnectTimeoutError:
            logger.info('连接超时')
        except exceptions.MaxRetryError:
            logger.info('超过最大尝试次数')
        except requests.exceptions.ProxyError:
            logger.info('代理错误，目标计算机积极拒绝')
        except requests.exceptions.ConnectTimeout:
            logger.info('连接超时')
        except Exception as e:
            logger.info(e)
        finally:
            if not resp:
                self.proxies_db.decr(proxy)
        if not resp:
            return
        # print(resp.status)
        if resp.status in [200]:
            self.proxies_db.set_max(proxy)
        else:
            self.proxies_db.decr(proxy)
    async def get(self):
        self.aio_redis=await self.aio_proxies_db.get_redis()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}
        async with aiohttp.ClientSession() as self.session:
            # while self.proxies_db.count():
            for _ in range(2):
                tasks=[asyncio.ensure_future(self.get_resp(headers)) for _ in range(SAME_EVENT_NUM)]
                await asyncio.wait(tasks)
    def async_start_proxies_ready(self):
        start=time.perf_counter()
        self.loop = asyncio.get_event_loop()
        task=asyncio.ensure_future(self.get())
        self.loop.run_until_complete(task)
        # self.loop.run_forever()
        end=time.perf_counter()
        print(end-start,'秒')
    def start(self):
        if OPEN_PROXIES:
            # self.spiders=self.auto_import(PROXIES_SPIDERS, isspider=True)
            # self.pipeline=self.auto_import(PROXIES_PIPELINE)
            # self.start_spider()
            # exit()
            if not PROXIES_ASYNC:
                self.start_proxies_ready()
            else:

                self.async_start_proxies_ready()




        else:
            self.start_spider()
