# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        if spider.name == 'sjru':
            item['salary'] = self.salary_superjob(item['salary'])
        if spider.name == 'hhru':
            item['salary'] = self.salary_hh(item['salary'])

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def salary_superjob(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        for i in range(len(salary)):
            salary[i] = salary[i].replace(u'\xa0', u' ')

        if salary[0] == 'до':
            salary[2] = salary[2].split(' ')
            salary_currency = salary[2][-1]
            salary_max = salary[2][0] + salary[2][1]
        elif salary[0] == 'от':
            salary[2] = salary[2].split(' ')
            salary_currency = salary[2][-1]
            salary_min = salary[2][0] + salary[2][1]
        elif len(salary) > 3:
            salary_min = salary[0]
            salary_max = salary[1]
            salary_currency = salary[3]
        elif len(salary) == 3:
            salary_min = salary[0]
            salary_max = salary[0]
            salary_currency = salary[2]

        result = [salary_min, salary_max, salary_currency]
        return result

    def salary_hh(self, salary):
        salary_min = None
        salary_max = None
        salary_currency = None

        for i in range(len(salary)):
             salary[i] = salary[i].replace(u'\xa0', u' ')

        if salary[2] == ' до ':
            salary_min = salary[1]
            salary_max = salary[3]
            salary_currency = salary[-2]
        elif salary[0] == 'от ':
            salary_min = salary[1]
            salary_currency = salary[-2]
        elif salary[0] == 'до ':
            salary_currency = salary[-1]
            salary_max = salary[1]

        result = [salary_min, salary_max, salary_currency]
        return result