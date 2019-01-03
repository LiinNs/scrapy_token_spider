# -*- coding: utf-8 -*-
import scrapy
from token_pipeline.items import ImageItem


class CoinSpider(scrapy.Spider):
    name = 'coin'

    custom_settings = {
        # 指定使用的 Pipeline
        'ITEM_PIPELINES': {
            'token_pipeline.pipelines.TokenFilesPipeline': 1,
        }
    }

    def start_requests(self):
        urls = [
            'https://info.binance.com/en/currencies/bitcoin'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_image_url, meta={'proxy': 'http://127.0.0.1:1087'})

    def parse_image_url(self, response):
        item = ImageItem()
        item['name'] = response.css('div.ix71fe-1.haNgdx > div.left-wapper > div.media-info > div.media-heading >div.instro::text').extract_first()
        item['url'] = response.css('div.ix71fe-1.haNgdx > div.left-wapper > img::attr(src)').extract_first()
        yield item

