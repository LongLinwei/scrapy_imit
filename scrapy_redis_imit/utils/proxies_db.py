import redis
from scrapy_redis_imit.config.setting import PROXIES_REDIS_HOST, PROXIES_REDIS_PORT, PROXIES_REDIS_DB, PROXIES_REDIS_PASSWD, PROXIES_REDIS_NAME, \
    MAX_SCORE, MIN_SCORE, INIT_SCORE
from random import choice
from scrapy_redis_imit.utils.log import logger

class ProxiesDb:
    def __init__(self, host=PROXIES_REDIS_HOST, port=PROXIES_REDIS_PORT, db=PROXIES_REDIS_DB, passwd=PROXIES_REDIS_PASSWD,
                 name=PROXIES_REDIS_NAME):
        self.redis = redis.Redis(host=host, port=port, db=db, password=passwd)
        self.name = name

    def add(self, proxy, score=INIT_SCORE):
        if not self.redis.zscore(self.name, proxy):
            if self.redis.zadd(self.name, {proxy: INIT_SCORE}):
                logger.info(f"添加<{proxy}>成功")
        else:
            logger.info(f"<{proxy}>已存在")

    def get(self):
        result = self.redis.zrangebyscore(self.name, MAX_SCORE, MAX_SCORE)
        if result:
            return choice(result)
        else:
            result = self.redis.zrevrangebyscore(self.name, MAX_SCORE, MIN_SCORE)[:20]
            if result:
                return choice(result)
            else:
                logger.info('代理池空空如也')
                return
    def first_get(self):
        result = self.redis.zrangebyscore(self.name, MIN_SCORE, MAX_SCORE)
        if result:
            return choice(result)
        else:
            result = self.redis.zrevrangebyscore(self.name, MAX_SCORE, MIN_SCORE)[:20]
            if result:
                return choice(result)
            else:
                logger.info('代理池空空如也')
                return

    def set_max(self, proxy):
        self.redis.zadd(self.name, {proxy: MAX_SCORE})
        logger.info(f'已将<{proxy}>分数调至100')

    def decr(self, proxy):
        score = self.redis.zscore(self.name, proxy)
        if score and score > MIN_SCORE+1:
            score=self.redis.zincrby(self.name, -1, proxy)
            logger.info(f'<{proxy}>分数下调至{score}分')
        else:
            logger.info(f'{proxy}分数为0，移除')
            self.redis.zrem(self.name, proxy)


    def exist(self, proxy):
        return self.redis.zscore(self.name, proxy) is not None

    def count(self):
        return self.redis.zcard(self.name)

    def all(self):
        return self.redis.zrangebyscore(self.name, MIN_SCORE, MAX_SCORE)
    def score(self,proxy):
        return self.redis.zscore(self.name,proxy)
