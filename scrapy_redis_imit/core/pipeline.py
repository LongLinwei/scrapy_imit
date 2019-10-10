class Pipeline:
    def process_item(self, item):
        print(item.data.decode()[:1000])
        return item
