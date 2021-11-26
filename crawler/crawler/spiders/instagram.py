import json, scrapy, logging
from crawler.crawler.items import InstagramItem

class Instagram(scrapy.Spider):
    name = 'instagram'

    def __init__(self, filepath='crawler/spiders/IDs.json', first=12, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        # Get posts
        self.posts_url = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables={{"id":"{0}","first":{1},"after":"{2}"}}'
        # Get comments
        self.comments_url = 'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={{"shortcode":"{0}","first":{1},"after":"{2}"}}'
        # Number of endpoints
        self.first = first
        self.standard_after = '{\\"cached_comments_cursor\\": \\"\\", \\"bifilter_token\\": \\"\\"}'



    def start_requests(self):
        with open(self.filepath, 'r') as f:
            IDs = json.load(f)

        # Create URL's for profiles
        for ID in IDs:
            url = self.posts_url.format(ID, self.first, self.standard_after)
            yield scrapy.Request(url=url,  callback=self.parse,
                                 cookies={})



    def parse(self, response):
        item = InstagramItem()
        # Iterate through posts, extract shortcodes for comment URL's
        for edge in response['data']['user']['edge_owner_to_timeline_media']['edges']:
            # Scrape posts
            next_page = self.comments_url.format(edge['node']['shortcode'], self.first, self.standard_after)
            yield scrapy.Request(url=next_page, callback=self.parse_comments,
                                 cookies={})



    def parse_comments(self, response):
        item = InstagramItem()
        # Extract comment data
        for edge in response['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            item['username'] = edge['node']['owner']['username']
            item['id'] = edge['node']['owner']['id']
            item['text'] = edge['node']['text']
            yield item
