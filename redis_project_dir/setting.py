import logging

#日志设置
DEFAULT_LOG_LEVEL = logging.INFO  # 日志等级
DEFAULT_LOG_FMT = '%(asctime)s %(name)s %(filename)s %(funcName)s %(levelname)s<%(lineno)d>%(message)s'  # 日志格式
DEFAULT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 时间格式
DEFAULT_LOG_FILENAME = 'log.log'  # 日志存放地址

# 爬虫启用
SPIDERS = [
    # 'spiders.baiduspider.BaiduSpider',
    'spiders.guoke_spider.GuokeSpider',
    # 'spiders.xinlang.XinlangSpider',
]

# 下载中间键启用
DOWNLODER_MIDDLEWARES = [
    'downloder_middleware.DownloderMiddleware'
]

# 爬虫中间键启用
SPIDER_MIDDLEWARES = [
    # 'spider_middleware.SpiderMiddleware'
]

# 管道启用
PIPELINE = [
    # 'pipeline.BaiduPipeline',
    'pipeline.GuokePipeline'
    # 'pipeline.XinlangPipeline',

]
#是否启用多线程
OPEN_PROCESSING=True
# 线程数量设置
PROCESSING_NUM = 4

# redis设置

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWD = None
# redis queue set键名
REDIS_QUEUE_NAME = 'queue'
REDIS_BACKUPQUEUE_NAME='backupqueue'
REDIS_SET_NAME='redis_set'
#爬虫使用代理池
USE_PROXY=True
#代理ip相关设置

    # 代理ip爬虫
PROXIES_SPIDERS = [
    # 'proxies.proxy_spider.ProxySpider',
    # 'proxies.proxy_spider.KuaiSpider',
    # 'proxies.proxy_spider.EightSpider'
# 'proxies.proxy_spider.IphaiSpider'
# 'proxies.proxy_spider.XilaSpider'
'proxies.proxy_spider.NimaSpider'
]

PROXIES_PIPELINE=[
    'proxies.proxy_pipeline.ProxyPipeline'
]

    #代理ip爬前预热开关
OPEN_PROXIES=True
#使用异步
PROXIES_ASYNC=True
#一次事务提交数量
SAME_EVENT_NUM=10000
READY_URL='http://www.baidu.com'

    #代理ip db设置
PROXIES_REDIS_HOST = 'localhost'
PROXIES_REDIS_PORT = 6379
PROXIES_REDIS_DB = 1
PROXIES_REDIS_PASSWD = None
PROXIES_REDIS_NAME='proxies_db'
MAX_SCORE=100
MIN_SCORE=0
INIT_SCORE=5

#请求重试次数
RETRY_NUM=3