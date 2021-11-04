# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    username = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
    shortcode = scrapy.Field()
    caption = scrapy.Field()
