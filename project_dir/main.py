from scrapy_imit.core.engine import Engine
from project_dir.spiders.baiduspider import BaiduSpider
from project_dir.spiders.guoke_spider import GuokeSpider
if __name__=="__main__":
    # spiders={BaiduSpider.name:BaiduSpider(),GuokeSpider.name:GuokeSpider()}
    engine=Engine()
    engine.start()