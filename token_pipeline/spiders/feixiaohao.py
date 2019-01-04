# -*- coding: utf-8 -*-
import scrapy
import json
from token_pipeline.items import ImageItem
from os.path import splitext


class FeixiaohaoSpider(scrapy.Spider):
    name = 'feixiaohao'
    allowed_domains = ['feixiaohao.com']

    custom_settings = {
        # 指定使用的 Pipeline
        'ITEM_PIPELINES': {
            'token_pipeline.pipelines.TokenFilesPipeline': 1,
        }
    }

    start_urls = ['https://dncapi.feixiaohao.com/api/coin/data_list']

    def parse(self, response):
        js = json.loads(response.body)
        for coin in js['data']:
            item = ImageItem()
            item['name'] = coin['name']
            item['sort_name'] = coin["symbol"]
            item['url'] = coin['logo']
            filename, file_extension = splitext(item['url'])
            item['image_name'] = item['name'] + file_extension
            yield item
