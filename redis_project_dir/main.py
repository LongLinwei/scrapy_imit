from scrapy_redis_imit.core.engine import Engine

if __name__ == "__main__":
    # spiders={BaiduSpider.name:BaiduSpider(),GuokeSpider.name:GuokeSpider()}
    engine = Engine()
    engine.start()
