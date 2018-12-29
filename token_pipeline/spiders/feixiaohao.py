# -*- coding: utf-8 -*-
import scrapy


class FeixiaohaoSpider(scrapy.Spider):
    name = 'feixiaohao'
    allowed_domains = ['feixiaohao.com']
    start_urls = ['http://feixiaohao.com/']

    def parse(self, response):
        pass
