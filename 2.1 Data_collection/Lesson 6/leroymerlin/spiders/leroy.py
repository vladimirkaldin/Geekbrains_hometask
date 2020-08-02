# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}']

    def parse(self, response):
        links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.parse_link)

        next_page = response.xpath("//a[@class='paginator-button next-paginator-button']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def parse_link(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name',"//h1/text()")
      #  loader.add_xpath('photos',"//img[@alt='product image']/@src")
        loader.add_xpath('photos_urls', "//img[@alt='product image']/@src")
        loader.add_xpath('price', "//uc-pdp-price-view[1]/span/text()")
        loader.add_css('params_name', 'dt.def-list__term ::text')
        loader.add_css('params_definition', 'dd.def-list__definition ::text')
        loader.add_value('link', response.url)
        yield loader.load_item()
