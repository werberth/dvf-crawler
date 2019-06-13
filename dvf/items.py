import re
import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def filter_price(value):
    for character in "$,.":
        value = value.replace(character, '')
    return value.strip()


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
    price = scrapy.Field(
        input_processor=MapCompose(filter_price)
    )
    stock = scrapy.Field()
