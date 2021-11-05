import json, scrapy, logging

from crawler.items import InstagramItem

class Instagram(scrapy.Spider):
    name = 'instagram'

    def __init__(self, filepath='crawler/spiders/IDs.json', first=12, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        # get posts
        self.posts_url = 'https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables={{"id":"{0}","first":{1},"after":"{2}"}}'
        # get comments
        self.comments_url = 'https://www.instagram.com/graphql/query/?query_hash=bc3296d1ce80a24b1b6e40b1e72903f5&variables={{"shortcode":"{0}","first":{1},"after":"{2}"}}'
        # number of endpoints
        self.first = first
        self.standard_after = '{\\"cached_comments_cursor\\": \\"\\", \\"bifilter_token\\": \\"\\"}'



    def start_requests(self):
        with open(self.filepath, 'r') as f:
            IDs = json.load(f)

        # create URL's for profiles
        for ID in IDs:
            url = self.posts_url.format(ID, self.first, self.standard_after)
            yield scrapy.Request(url=url,  callback=self.parse,
                                 cookies={'csrftoken': 'rPv7XKXSDzpopZzKzHSsD2K8aXNYOR6i',
                                          'datr': 'DbJYYVGxT4ij2e6mxW6pGpKx',
                                          'ds_user_id': '49833673560',
                                          'ig_did': 'EC4F4E00-D29B-4951-8455-F0FC6E5D4185',
                                          'mid': 'YVXmyAALAAGN73VoK3-lG9B_klr5',
                                          'sessionid': '49833673560%3Ac5gSLvrClQbd4L%3A15',
                                          'shbid': '"3776\\0542075502672\\0541667403400:01f7eb6903eb647e4d2e5a9e64215d5f10311bb5aa5f528e0e3257d0c0643c2b579583a7"',
                                          'shbts': '"1635867400\\0542075502672\\0541667403400:01f785f66992392e6a6abd0d7ee09d392f0b73696c03291a48601b4e670c6eea898cc883"'})



    def parse(self, response):
        item = InstagramItem()
        # iterate through posts, extract shortcodes for comment URL's
        for edge in response['data']['user']['edge_owner_to_timeline_media']['edges']:
            # scrape posts
            next_page = self.comments_url.format(edge['node']['shortcode'], self.first, self.standard_after)
            yield scrapy.Request(url=next_page, callback=self.parse_comments,
                                 cookies={'csrftoken': 'rPv7XKXSDzpopZzKzHSsD2K8aXNYOR6i',
                                          'datr': 'DbJYYVGxT4ij2e6mxW6pGpKx',
                                          'ds_user_id': '49833673560',
                                          'ig_did': 'EC4F4E00-D29B-4951-8455-F0FC6E5D4185',
                                          'mid': 'YVXmyAALAAGN73VoK3-lG9B_klr5',
                                          'sessionid': '49833673560%3Ac5gSLvrClQbd4L%3A15',
                                          'shbid': '"3776\\0542075502672\\0541667403400:01f7eb6903eb647e4d2e5a9e64215d5f10311bb5aa5f528e0e3257d0c0643c2b579583a7"',
                                          'shbts': '"1635867400\\0542075502672\\0541667403400:01f785f66992392e6a6abd0d7ee09d392f0b73696c03291a48601b4e670c6eea898cc883"'})



    def parse_comments(self, response):
        item = InstagramItem()
        # extract comment data
        for edge in response['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            item['username'] = edge['node']['owner']['username']
            item['id'] = edge['node']['owner']['id']
            item['text'] = edge['node']['text']
            yield item
