import logging

#日志设置
DEFAULT_LOG_LEVEL = logging.INFO  # 日志等级
DEFAULT_LOG_FMT = '%(asctime)s %(name)s %(filename)s %(funcName)s %(levelname)s<%(lineno)d>%(message)s'  # 日志格式
DEFAULT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 时间格式
DEFAULT_LOG_FILENAME = 'log.log'  # 日志存放地址

# 爬虫启用
SPIDERS = [
    'spiders.baiduspider.BaiduSpider',
    'spiders.guoke_spider.GuokeSpider'
]

# 下载中间键启用
DOWNLODER_MIDDLEWARES = [
    # 'downloder_middleware.DownloderMiddleware'
]

# 爬虫中间键启用
SPIDER_MIDDLEWARES = [
    # 'spider_middleware.SpiderMiddleware'
]

# 管道启用
PIPELINE = [
    'pipeline.BaiduPipeline',
    'pipeline.GuokePipeline'
]
#是否启用多线程
OPEN_PROCESSING=True
# 线程数量设置
PROCESSING_NUM = 4