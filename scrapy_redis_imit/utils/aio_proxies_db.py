import aioredis
from scrapy_redis_imit.config.setting import PROXIES_REDIS_HOST, PROXIES_REDIS_PORT, PROXIES_REDIS_DB, PROXIES_REDIS_PASSWD, PROXIES_REDIS_NAME, \
    MAX_SCORE, MIN_SCORE, INIT_SCORE
from random import choice
from scrapy_redis_imit.utils.log import logger

class AioProxiesDb:
    def __init__(self, host=PROXIES_REDIS_HOST, port=PROXIES_REDIS_PORT, db=PROXIES_REDIS_DB, passwd=PROXIES_REDIS_PASSWD,
                 name=PROXIES_REDIS_NAME):
        self.host=host
        self.port=port
        self.db=db
        self.passwd=passwd
        self.name = name
    async def get_redis(self):
        self.redis =await aioredis.create_redis_pool((self.host,self.port), db=self.db, password=self.passwd)
        return self.redis
    async def add(self, proxy, score=INIT_SCORE):
        if not await self.redis.execute('zscore',self.name, proxy):
            if await self.redis.execute('zadd',self.name, {proxy: INIT_SCORE}):
                logger.info(f"添加<{proxy}>成功")
        else:
            logger.info(f"<{proxy}>已存在")

    async def get(self):
        result = await self.redis.execute('zrangebyscore',self.name, MAX_SCORE, MAX_SCORE)
        if result:
            return choice(result)
        else:
            result = await self.redis.execute('zrevrangebyscore',self.name, MAX_SCORE, MIN_SCORE)[:20]
            if result:
                return choice(result)
            else:
                logger.info('代理池空空如也')
                return
    async def first_get(self):
        result = await self.redis.zrangebyscore(self.name, MIN_SCORE, MAX_SCORE)
        if result:
            return choice(result)
        else:
            result =await self.redis.zrevrangebyscore(self.name, MAX_SCORE, MIN_SCORE)[:20]
            if result:
                return choice(result)
            else:
                logger.info('代理池空空如也')
                return

    async def set_max(self, proxy):
        await self.redis.zadd(self.name, {proxy: MAX_SCORE})
        logger.info(f'已将<{proxy}>分数调至100')

    async def decr(self, proxy):
        score =await self.redis.zscore(self.name, proxy)
        if score and score > MIN_SCORE+1:
            score=await self.redis.zincrby(self.name, -1, proxy)
            logger.info(f'<{proxy}>分数下调至{score}分')
        else:
            logger.info(f'{proxy}分数为0，移除')
            await self.redis.zrem(self.name, proxy)


    async def exist(self, proxy):
        return await self.redis.zscore(self.name, proxy) is not None

    async def count(self):
        return await self.redis.zcard(self.name)

    async def all(self):
        return await  self.redis.zrangebyscore(self.name, MIN_SCORE, MAX_SCORE)
    async def score(self,proxy):
        return await  self.redis.zscore(self.name,proxy)
