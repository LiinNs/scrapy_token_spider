# -*- coding: utf-8 -*-
import scrapy


class BinanceSpider(scrapy.Spider):
    name = 'binance'

    def start_requests(self):
        urls = [
            'https://info.binance.com/en/all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'http://127.0.0.1:1087'})

    def parse(self, response):
        for coin in response.css('div.s7v36e6-0.eJTsoN > div.name > span.fullName::text').extract():
            detail_page = "https://info.binance.com/cn/currencies/%s" %  coin.replace(' ', '-')
            yield scrapy.Request(detail_page, callback=self.parse_image, meta={'proxy': 'http://127.0.0.1:1087'})

    def parse_image(self, response):
        yield {
            'coin': response.css('div.ix71fe-1.haNgdx > div.left-wapper > div.media-info > div.media-heading >div.instro::text').extract_first(),
            'image_url': response.css('div.ix71fe-1.haNgdx > div.left-wapper > img::attr(src)').extract_first(),
        }
