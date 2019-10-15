import redis

# REDIS_COUNT_HOST = 'localhost'
# REDIS_COUNT_PORT = 6379
# REDIS_COUNT_DB = 0
# REDIS_COUNT_PASSWD =
from scrapy_redis_imit.config.setting import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWD


class Count:
    total_request_name = "total_request"
    total_resp_name = "total_resp"
    total_repeat_request_name = "total_repeat_request"
    start_spider_num_name = "start_spider_num"
    fail_request_num_name = 'fail_request_num_name'

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, passwd=REDIS_PASSWD):
        self.redis = redis.Redis(host=host, port=port, db=db, password=passwd)

    def _get_total_request(self):
        return self.redis.get(self.total_request_name)

    def _get_total_resp(self):
        return self.redis.get(self.total_resp_name)

    def _get_total_repeat_request(self):
        return self.redis.get(self.total_repeat_request_name)

    def _get_start_spider_num(self):
        return self.redis.get(self.start_spider_num_name)

    def _get_fail_request_num(self):
        return self.redis.get(self.fail_request_num_name)

    @property
    def total_request(self):
        return int(self._get_total_request()) if self._get_total_request() else 0

    @property
    def total_resp(self):
        return int(self._get_total_resp()) if self._get_total_resp() else 0

    @property
    def total_repeat_request(self):
        return int(self._get_total_repeat_request()) if self._get_total_repeat_request() else 0

    @property
    def start_spider_num(self):
        return int(self._get_start_spider_num()) if self._get_start_spider_num() else 0

    @property
    def fail_request_num(self):
        return int(self._get_fail_request_num()) if self._get_fail_request_num() else 0

    def incr_total_request(self):
        self.redis.incr(self.total_request_name)

    def incr_total_resp(self):
        self.redis.incr(self.total_resp_name)

    def incr_total_repeat_request(self):
        self.redis.incr(self.total_repeat_request_name)

    def incr_start_spider_num(self):
        self.redis.incr(self.start_spider_num_name)

    def incr_fail_request_num(self):
        self.redis.incr(self.fail_request_num_name)

    def clear(self):
        self.redis.delete(self.total_request_name)
        self.redis.delete(self.total_resp_name)
        self.redis.delete(self.total_repeat_request_name)
        self.redis.delete(self.start_spider_num_name)
        self.redis.delete(self.fail_request_num_name)
