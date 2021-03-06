import redis
import pickle

# REDIS_QUEUE_HOST = 'localhost'
# REDIS_QUEUE_PORT = 6379
# REDIS_QUEUE_DB = 0
# REDIS_QUEUE_PASSWD = None
# REDIS_QUEUE_NAME = 'queue'
from scrapy_redis_imit.config.setting import REDIS_HOST,REDIS_PORT,REDIS_DB,REDIS_PASSWD,REDIS_QUEUE_NAME,REDIS_BACKUPQUEUE_NAME


class Queue:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, passwd=REDIS_PASSWD,
                 name=REDIS_QUEUE_NAME):
        self.redis = redis.Redis(host=host, port=port, db=db, password=passwd)
        self.name = name

    def put(self, request):
        self.redis.rpush(self.name, pickle.dumps(request))

    def get(self):
        request = self.redis.lpop(self.name)
        if request:
            return pickle.loads(request)

class BackupQueue:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, passwd=REDIS_PASSWD,
                 name=REDIS_BACKUPQUEUE_NAME):
        self.redis = redis.Redis(host=host, port=port, db=db, password=passwd)
        self.name = name

    def put(self, request):
        self.redis.rpush(self.name, pickle.dumps(request))

    def pop(self):
        request = self.redis.lpop(self.name)
        if request:
            return pickle.loads(request)

    def llen(self):
        return self.redis.llen(self.name)

    def rpoplpush(self):
        self.redis.rpoplpush(self.name,REDIS_QUEUE_NAME)