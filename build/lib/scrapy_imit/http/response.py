from lxml import etree
import re
import json


class Response:
    def __init__(self, url, status, headers, data, request, meta=None):
        self.url = url
        self.status = status
        self.headers = headers
        self.data = data
        self.request = request
        self.meta = meta

    def xpath(self, pattern):
        html = etree.HTML(self.data.decode())
        return html.xpath(pattern)

    def re(self, pattern):
        return re.findall(pattern, self.data.decode())

    def json(self):
        return json.loads(self.data)
