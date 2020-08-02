# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from scrapy.exceptions import DropItem
from urllib.parse import urlparse
import os

class LeroymerlinPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item['params'] = dict(zip(item['params_name'], item['params_definition']))
        item.pop('params_name')
        item.pop('params_definition')
        collection.insert_one(item)
        return item

class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        s = 'images/' + item['link'].split('/')[-2].replace('-', '_')
        os.mkdir(s)
        for photo_url in item['photos_urls']:
            yield scrapy.Request(photo_url)

    def file_path(self, request, response=None, info=None):
        file_name = os.path.basename(urlparse(request.url).path)
        path = os.getcwd() + '\images'
        product_list = [i[0] for i in os.walk(path)]
        for y in product_list:
            if y[-8:] == file_name[:8]:
                product = y.split('\\')[-1]
                return f'{product}/{file_name}'

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("No image found")
        item['photos_paths'] = image_paths
        return item