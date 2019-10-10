from lxml import etree
import re
import json


class Response:
    def __init__(self, url, status, headers, text,content, request, meta=None):
        self.url = url
        self.status = status
        self.headers = headers
        self.text = text
        self.content=content
        self.request = request
        self.meta = meta

    def xpath(self, pattern):
        html = etree.HTML(self.content.decode())
        return html.xpath(pattern)

    def re(self, pattern):
        return re.findall(pattern, self.content.decode())

    def json(self):
        return json.loads(self.content)
