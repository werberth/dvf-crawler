import re
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class TakeFirstItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class DressItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    brandId = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    color = scrapy.Field(output_processor=TakeFirst())
    variants = scrapy.Field()


class SizeItem(scrapy.Item):
    size = scrapy.Field(default=None)
    color = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
