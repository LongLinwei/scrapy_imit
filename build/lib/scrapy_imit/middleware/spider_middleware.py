class SpiderMiddleware:
    def process_request(self, request):
        print('spider_mid:process request')
        return request

    def process_response(self, response):
        print("spider_midd:process response")
        return response
