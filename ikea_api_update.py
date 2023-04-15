from ikea_update.spiders.ikea import IkeaSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    settiings=get_project_settings()
    process = CrawlerProcess(settings=settiings)
    process.crawl(IkeaSpider)
    process.start()
    
if __name__ == '__main__':
    main()
