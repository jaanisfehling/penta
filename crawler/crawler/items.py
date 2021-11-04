import scrapy


class CommentItem(scrapy.Item):
    username = scrapy.Field()
    id = scrapy.Field()
    text = scrapy.Field()
    shortcode = scrapy.Field()
    caption = scrapy.Field()
