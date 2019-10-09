class DownloderMiddleware:
    def process_request(self,request):
        print('downloder_mid:process request')
        return request
    def process_response(self,response):
        print("downloder_midd:process response")
        return response