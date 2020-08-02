# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose,Compose, Join
import re

def cleaner_link(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def price_to_int(values):
    return int(values.replace(' ', ''))

def cleaner(values):
    pattern = re.compile('[\w\(\),\.\+\/.]+')
    return (' '.join(pattern.findall(values)))

class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_link))
    price = scrapy.Field(input_processor=TakeFirst(), output_processor=MapCompose(price_to_int))
    params_name = scrapy.Field()
    params_definition = scrapy.Field(input_processor=MapCompose(cleaner))
    params = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    photos_urls = scrapy.Field()
    photos = scrapy.Field()
    photos_paths = scrapy.Field()

