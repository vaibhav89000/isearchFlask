from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from searchdetail.spiders.search import SearchSpider


process = CrawlerProcess(get_project_settings())
process.crawl(SearchSpider)
process.start()
