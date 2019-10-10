from scrapy_imit.core.pipeline import Pipeline


class BaiduPipeline(Pipeline):
    def process_item(self, item, spider):
        if spider.name == 'baidu':
            print('百度数据：')
            print(item.data.decode()[:100])
        return item


class GuokePipeline(Pipeline):
    def process_item(self, item, spider):
        if spider.name == 'guoke':
            print('果壳数据：')
            print(item.data)
        return item
