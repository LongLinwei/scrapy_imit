from scrapy_redis_imit.core.pipeline import Pipeline
import json

class BaiduPipeline(Pipeline):
    def process_item(self, item, spider):
        if spider.name == 'baidu':
            print('百度数据：')
            print(item.data[:100])
        return item


class GuokePipeline(Pipeline):
    def process_item(self, item, spider):
        if spider.name == 'guoke':
            print('果壳数据：')
            print(item.data)
        return item

class XinlangPipeline(Pipeline):
    def process_item(self, item, spider):
        if spider.name == 'xinlang':
            print('新浪数据：')
            print(item.data)
        return item


