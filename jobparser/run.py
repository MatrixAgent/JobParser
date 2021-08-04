from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

#from jobparser import settings
#from jobparser.spiders.hh_ru import HhRuSpider
import jobparser.settings
from jobparser.spiders.jobs import JobsSpider
from jobparser.spiders.jobs2 import Jobs2Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(jobparser.settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(JobsSpider)
    process.crawl(Jobs2Spider)

    process.start()
