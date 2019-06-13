# -*- coding: utf-8 -*-
import scrapy

from scrapy.loader import ItemLoader

from dvf.items import DressItem, SizeItem, TakeFirstItemLoader


class DressesSpider(scrapy.Spider):
    name = 'dresses'
    allowed_domains = ['www.dvf.com', 'world.dvf.com', 'eu.dvf.com']
    start_urls = ['https://www.dvf.com/']

    def parse(self, response):
        dresses_url = response.xpath(
            "//ul/li[contains(@id, 'sub-menu_dresses-all')]/a/@href"
        )
        yield scrapy.Request(
            url=dresses_url.get(),
            callback=self.parse_dresses
        )

    def parse_dresses(self, response):
        dresses = response.xpath(
            "//div[contains(@class, 'product-image')]/a/@href"
        )
        for url in dresses.getall():
            yield scrapy.Request(
                url=url,
                callback=self.parse_dress
            )

        next_page = response.xpath(
            "//div[contains(@class, 'infinite-scroll-placeholder')]"
            "/@data-grid-url"
        )
        next_page = next_page.get()

        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_dresses
            )

    def parse_dress(self, response):
        """
            Get informations about one dress.
        """

        loader = ItemLoader(DressItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_value("brandId", "dvf")
        loader.add_xpath(
            "name",
            "//h1[contains(@class, 'product-overview-title')]/text()"
        )
        loader.add_xpath(
            "description",
            "//div[contains(@class, 'product-module short-desc')]/p/text()"
        )
        loader.add_xpath(
            "images",
            "//div[contains(@id, 'pdp-image-container')]"
            "/div[contains(@class, 'js-vertical-slide')]/img/@src"
        )
        loader.add_xpath(
            "color",
            "//div/span[contains(@class, 'selectedColorName')]/text()"
        )

        item = loader.load_item()
        item["variants"] = []

        sizes = response.xpath(
            "//div[@class='pdp-size-select-wrapper']"
            "//div[contains(@class, 'selectableSize')]/"
            "a[contains(@class, 'size-link')]/div/text()"
        )
        sizes = sizes.getall()

        for size in sizes:
            self.parse_variants(item, size, response)

        if not sizes:
            self.parse_variants(item, None, response)

        yield item

    def parse_variants(self, item, size, response):
        """
            Get informations about one size.
        """

        loader = TakeFirstItemLoader(SizeItem(), response=response)
        loader.add_xpath(
            "price",
            "//div[contains(@class, 'product-overview-price ')]/span/text()"
        )
        loader.add_xpath(
            "color",
            "//div/span[contains(@class, 'selectedColorName')]/text()"
        )
        loader.add_xpath(
            "stock",
            "boolean(//div[contains(@class,'selectable selectableSizeParent available')]"
            "[@data-attrsize='{}'])".format(size)
        )

        variant = loader.load_item()
        variant["size"] = size

        item['variants'].append(variant)
