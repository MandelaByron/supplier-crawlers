# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IkeaUpdateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    scrap_url = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    product_code = scrapy.Field()
    price = scrapy.Field()
    list_price = scrapy.Field()
    qty = scrapy.Field()

