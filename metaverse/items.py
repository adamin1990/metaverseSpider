# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MetaverseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    # 引用地址
    quote = scrapy.Field()
    # 2 nft 1 元宇宙
    type = scrapy.Field()
    mContent = scrapy.Field()

