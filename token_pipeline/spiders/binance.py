# -*- coding: utf-8 -*-
import scrapy
from token_pipeline.items import ImageItem
from os.path import splitext


class BinanceSpider(scrapy.Spider):
    name = 'binance'

    # custom_settings = {
    #     # 指定使用的 Pipeline
    #     'ITEM_PIPELINES': {
    #         'token_pipeline.pipelines.CoinImagePipeline': 1,
    #     }
    # }

    def start_requests(self):
        urls = [
            'https://info.binance.com/en/all'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'http://127.0.0.1:1087'})

    def parse(self, response):
        for coin in response.css('div.s7v36e6-0.eJTsoN > div.name > span.fullName::text').extract():
            detail_page = "https://info.binance.com/cn/currencies/%s" %  coin.strip().replace(' ', '-')
            yield scrapy.Request(detail_page, callback=self.parse_image_url, meta={'proxy': 'http://127.0.0.1:1087'})

    def parse_image_url(self, response):
        item = ImageItem()
        item['name'] = response.css('div.ix71fe-1.haNgdx > div.left-wapper > div.media-info > div.media-heading >div.instro::text').extract_first()
        item['sort_name'] = response.css('div.ix71fe-1.haNgdx > div.left-wapper > div.media-info > div.media-heading > h1::text').extract_first()
        item['url'] = response.css('div.ix71fe-1.haNgdx > div.left-wapper > img::attr(src)').extract_first()
        filename, file_extension = splitext(item['url'])
        item['image_name'] = item['name'] + file_extension
        yield item
