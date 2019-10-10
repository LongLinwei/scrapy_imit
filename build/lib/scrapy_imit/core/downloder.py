import requests
from scrapy_imit.http.response import Response
from scrapy_imit.utils.log import logger


class Downloder:
    total_resp = 0

    def get_resp(self, request):
        if request.method == 'GET':
            resp = requests.get(request.url, params=request.params, headers=request.headers)
        elif request.method == 'POST':
            resp = requests.post(url=request.url, data=request.data, params=request.params, headers=request.headers)
        else:
            logger.info('不支持的请求方法')
        logger.info("请求{}<{}>".format(request.url, resp.status_code))
        return Response(url=resp.url, status=resp.status_code, headers=resp.headers, data=resp.content, request=request)
