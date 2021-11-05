import scrapy


class InstagramItem(scrapy.Item):
    username = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
