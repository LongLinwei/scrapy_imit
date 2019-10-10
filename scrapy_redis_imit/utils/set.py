import redis
# REDIS_SET_HOST='localhost'
# REDIS_SET_PORT=6379
# REDIS_SET_DB=0
# REDIS_SET_PASSWD=None
# REDIS_SET_NAME='redis_set'
from scrapy_redis_imit.config.setting import REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_PASSWD,REDIS_SET_NAME

class RedisSet:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, passwd=REDIS_PASSWD,name=REDIS_SET_NAME):
        self.redis = redis.Redis(host=host, port=port, db=db, password=passwd)
        self.name=name
    def add(self,instruct):
        self.redis.sadd(self.name,instruct)
    def exist(self,key):
        return self.redis.sismember(self.name,key)
    def clear(self):
        self.redis.delete(self.name)