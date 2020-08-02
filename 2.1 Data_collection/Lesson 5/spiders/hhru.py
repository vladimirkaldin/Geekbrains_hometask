# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [f'https://hh.ru/search/vacancy?area=&st=searchVacancy&text={text}']

    def parse(self, response:HtmlResponse):
        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.css("div.vacancy-title h1::text").extract_first()
        salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        company = response.xpath("//span[@class='bloko-section-header-2 bloko-section-header-2_lite']/text()").extract()
        city = response.xpath("//p[@data-qa='vacancy-view-location']/text() | //span[@class='bloko-metro-pin']/text()").extract_first()
        link = response.url
        source = self.allowed_domains[0]
        yield JobparserItem(name=name, salary=salary, company=company, link=link, source=source, city=city)