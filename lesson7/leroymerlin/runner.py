from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from leroymerlin import settings
from leroymerlin.spiders.leroymerlinparser import LeroymerlinSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule(settings)

    process = CrawlerProcess(crawler_setting)
    query_str = input("Введите категории товаров: ")
    process.crawl(LeroymerlinSpider, query_str=query_str)

    process.start()
