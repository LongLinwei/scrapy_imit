import logging

# 日志设置
DEFAULT_LOG_LEVEL = logging.INFO  # 日志等级
DEFAULT_LOG_FMT = '%(asctime)s %(name)s %(filename)s %(funcName)s %(levelname)s<%(lineno)d>%(message)s'  # 日志格式
DEFAULT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 时间格式
DEFAULT_LOG_FILENAME = 'log.log'  # 日志存放地址

# 爬虫
SPIDERS = [

]

# 下载中间键
DOWNLODER_MIDDLEWARES = [

]

# 爬虫中间键
SPIDER_MIDDLEWARES = [

]

# 管道
PIPELINE = [

]

#是否启用多线程
OPEN_PROCESSING=False

# 线程数设置
PROCESSING_NUM = 4

# redis配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWD = None

REDIS_QUEUE_NAME = 'queue'
REDIS_BACKUPQUEUE_NAME='backupqueue'
REDIS_SET_NAME = 'redis_set'

#请求重试次数
RETRY_NUM=3