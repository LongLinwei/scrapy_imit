class Request:
    def __init__(self, url, method='GET', headers=None, data=None, params=None, spider_name=None, callback='parse',
                 meta=None,filter=True):
        self.url = url
        self.method = method.upper()
        self.headers = headers
        self.data = data
        self.params = params
        self.spider_name = spider_name
        self.callback = callback
        self.meta = meta
        self.filter=filter
