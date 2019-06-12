# -*- coding: utf-8 -*-
import scrapy


class DressesSpider(scrapy.Spider):
    name = 'dresses'
    allowed_domains = ['www.dvf.com', 'world.dvf.com']
    start_urls = ['https://www.dvf.com/']

    def parse(self, response):
        dresses_url = response.xpath("//ul/li[contains(@id, 'sub-menu_dresses-all')]/a/@href").get()
        yield scrapy.Request(
            url=dresses_url,
            callback=self.parse_dresses
        )
    
    def parse_dresses(self, response):
        dresses = response.xpath("//div[contains(@class, 'product-image')]/a/@href").getall()
        for url in dresses:
            yield scrapy.Request(
                url=url,
                callback=self.parse_data
            )

    def parse_data(self, response):
        url = response.url
        title = response.xpath("//h1[contains(@class, 'product-overview-title')]/text()").get()
        description = response.xpath("//div[contains(@class, 'product-module short-desc')]/p/text()").get()
        images = response.xpath("//div[contains(@id, 'pdp-image-container')]/div[contains(@class, 'js-vertical-slide')]/img/@src").getall()
        color = response.xpath("//div/span[contains(@class, 'selectedColorName')]/text()").get()

        data = {
            "brandId": "dvf",
            'url': url,
            'name': title,
            'color': color,
            'description': description,
            "images": images,
        }
        yield data
