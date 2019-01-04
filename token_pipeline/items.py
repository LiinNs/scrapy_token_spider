# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TokenPipelineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    name = scrapy.Field()
    sort_name = scrapy.Field()
    image_name = scrapy.Field()
    url = scrapy.Field()

class CoinInfoItem(scrapy.Item):
    code = scrapy.Field()
    key = scrapy.Field()
    issue_date = scrapy.Field()
    issue_price = scrapy.Field()
    website = scrapy.Field()
    white_paper = scrapy.Field()
    consensus_protocol = scrapy.Field()
    cryptographic_algorithm = scrapy.Field()
    source_code = scrapy.Field()
    max_supply = scrapy.Field()
    circulating_supply = scrapy.Field()
    introduction = scrapy.Field()

