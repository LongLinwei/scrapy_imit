class Response:
    def __init__(self, url, status, headers, data, request):
        self.url = url
        self.status = status
        self.headers = headers
        self.data = data
        self.request = request
