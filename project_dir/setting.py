import logging
DEFAULT_LOG_LEVEL=logging.INFO
DEFAULT_LOG_FMT='%(asctime)s %(name)s %(filename)s %(funcName)s %(levelname)s<%(lineno)d>%(message)s'
DEFAULT_LOG_DATEFMT='%Y-%m-%d %H:%M:%S'
DEFAULT_LOG_FILENAME='log.log'

SPIDERS=[
    'spiders.baiduspider.BaiduSpider',
    'spiders.guoke_spider.GuokeSpider'
]

DOWNLODER_MIDDLEWARES=[
    'downloder_middleware.DownloderMiddleware'
]
SPIDER_MIDDLEWARES=[
    'spider_middleware.SpiderMiddleware'
]

PIPELINE=[
    'pipeline.BaiduPipeline',
    'pipeline.GuokePipeline'
]