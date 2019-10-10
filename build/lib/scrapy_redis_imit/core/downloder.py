import requests
from scrapy_redis_imit.http.response import Response
from scrapy_redis_imit.utils.log import logger
from scrapy_redis_imit.config.setting import RETRY_NUM

class Downloder:
    # total_resp = 0

    def get_resp(self, request):
        for i in range(RETRY_NUM):
            if request.method == 'GET':
                resp = requests.get(request.url, params=request.params, headers=request.headers)
            elif request.method == 'POST':
                resp = requests.post(url=request.url, data=request.data, params=request.params, headers=request.headers)
            else:
                logger.info('不支持的请求方法')
            if resp.status_code in [200,301,302]:
                logger.info("请求 {}<{}>成功".format(request.url, resp.status_code))
                return Response(url=resp.url, status=resp.status_code, headers=resp.headers, text=resp.text,content=resp.content, request=request)
            else:
                logger.info("请求 {}<{}>失败，已重试次数{}".format(request.url, resp.status_code,request.retry_num))
                request.retry_num+=1