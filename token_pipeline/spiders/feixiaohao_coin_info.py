# -*- coding: utf-8 -*-
import scrapy
from token_pipeline.items import CoinInfoItem
import json


class FeixiaohaoCoinInfoSpider(scrapy.Spider):
    name = 'feixiaohao_coin_info'
    allowed_domains = ['feixiaohao.com']
    start_urls = ['https://dncapi.feixiaohao.com/api/coin/data_list']

    def parse(self, response):
        js = json.loads(response.body)
        for coin in js['data']:
            if coin['type'] == 1:
                url = "https://dncapi.feixiaohao.com/api/coin/web-coininfo"
                body = '{"code": "%s"}' % coin['code']
                headers = {'Content-Type': 'application/json; charset=utf-8'}
                yield scrapy.Request(url,\
                                     headers=headers,\
                                     method='POST',\
                                     body=body,\
                                     callback=self.parse_coin,\
                                     meta={'proxy': 'http://127.0.0.1:1087'})

    def parse_coin(self, response):
        js = json.loads(response.body)
        coin = js['data']
        item = CoinInfoItem()
        item['code'] = coin['symbol']
        item['key'] = coin['name']
        item['issue_date'] = coin['online_time']
        item['issue_price'] = coin['icoprice']
        item['website'] = coin['siteurl'].split("\\")[0]
        item['white_paper'] = coin['white_paper']
        item['source_code'] = coin['codelink']
        item['max_supply'] = coin['maxsupply']
        item['circulating_supply'] = coin['totalSupply']
        item['consensus_protocol'] = coin['prooftype']
        item['cryptographic_algorithm'] = coin['algorithm']
        item['introduction'] = coin['coindesc']
        yield item
