import requests
from scrapy_redis_imit.http.response import Response
from scrapy_redis_imit.utils.log import logger
from scrapy_redis_imit.config.setting import RETRY_NUM
from urllib3 import exceptions

class Downloder:
    # total_resp = 0
    def __init__(self,count,backupqueue,proxies_db):
        self.count=count
        self.backupqueue=backupqueue
        self.proxies_db=proxies_db
    def get_resp(self, request):
        for i in range(RETRY_NUM):
            resp=None
            if request.method == 'GET':
                try:
                    resp = requests.get(request.url, params=request.params, headers=request.headers,timeout=5)
                except ConnectionRefusedError:
                    logger.info('拒绝连接')
                except exceptions.ConnectTimeoutError:
                    logger.info('连接超时')
                except exceptions.MaxRetryError:
                    logger.info('超过最大尝试次数')
                except requests.exceptions.ProxyError:
                    logger.info('代理错误，目标计算机积极拒绝')
                except requests.exceptions.ConnectionError:
                    logger.info(request.url, "服务器拒绝访问")
                except requests.exceptions.ConnectTimeout:
                    logger.info(request.url, "连接超时")
                except Exception as e:
                    logger.info(request.url, "未知错误")
                finally:
                    if request.proxies:
                        # print(request.proxies['http'][7:])
                        self.proxies_db.decr(request.proxies['http'][7:])

            elif request.method == 'POST':
                try:
                    resp = requests.post(url=request.url, data=request.data, params=request.params, headers=request.headers)
                except Exception as e:
                    logger.info(request.url,e)
            else:
                logger.info('不支持的请求方法')
            if request.proxies:
                self.proxies_db.set_max(request.proxies['http'][7:])
            if not resp:
                return
            if resp.status_code in [200,301,302]:
                logger.info("请求 {}<{}>成功".format(request.url, resp.status_code))
                return Response(url=resp.url, status=resp.status_code, headers=resp.headers, text=resp.text,content=resp.content, request=request)

            else:
                logger.info("请求 {}<{}>失败，已重试次数{}".format(request.url, resp.status_code,request.retry_num))
                request.retry_num+=1
                if request.retry_num >= RETRY_NUM:
                    self.count.incr_fail_request_num()
                    self.backupqueue.pop()
