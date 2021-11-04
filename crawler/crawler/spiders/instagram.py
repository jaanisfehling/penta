import json, scrapy

class Instagram(scrapy.Spider):
    name = 'instagram'

    def __init__(self, filepath='crawler/spiders/IDs.json', first=50, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        # get posts
        self.posts_url = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables={"id":"{0}","first":{1},"after":"{2}"}'
        # get comments
        self.comments_url = 'https://www.instagram.com/graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables={"shortcode":"{0}","first":{1},"after":"{2}"}'
        # number of endpoints
        self.first = first
        self.standard_after = '{\"cached_comments_cursor\": \"\", \"bifilter_token\": \"\"}'



    def start_requests(self):
        with open(self.filepath, 'r') as f:
            IDs = json.load(f)

        # create URL's for profiles
        for ID in IDs:
            url = self.posts_url.format(ID, self.first, self.standard_after)
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):
        # extract shortcodes, captions
        for edge in response['data']['user']['edge_owner_to_timeline_media']['edges']:
            # (shortcode, caption)
            yield (edge['node']['shortcode'], edge['node']['edge_media_to_caption']['edges']['0']['node']['text'])
            # scrape posts
            url = self.comments_url.format(edge['node']['shortcode'], self.first, self.standard_after)
            yield scrapy.Request(url=url, callback=self.parse_post)



    def parse_post(self, response):
        # extract comments
        for edge in response['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            # ((username, id), text)
            yield ((edge['node']['owner']['username'], edge['node']['owner']['id']), edge['node']['text'])
