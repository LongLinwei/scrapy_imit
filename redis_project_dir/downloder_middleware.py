class DownloderMiddleware:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.204 Safari/537.36'}
    def process_request(self, request):
        request.headers=self.headers
        return request

    def process_response(self, response):
        # print("downloder_midd:process response")
        return response
