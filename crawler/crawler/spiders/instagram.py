import scrapy, json


class Instagram(scrapy.Spider):
    name = "instagram"
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {'json': 'scrapy.exporters.JsonItemExporter',},
        'FEED_EXPORT_ENCODING': 'utf-8'}


    def __init__(self, filepath="IDs.json", first=50, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        # get posts
        self.posts_url = """https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables={{"id":"{0}","first":{1},"after":"{2}"}}"""

        # get comments
        self.comments_url = """https://www.instagram.com/graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables={{"shortcode":"{0}","first":{1},"after":"{2}"}}"""

        # number of endpoints
        self.first = first

        self.standard_after = ""


    def start_requests(self):
        with open(self.filepath, "r") as f:
            IDs = json.load(f)

        # scrape profiles
        for ID in IDs:
            url = self.posts_url.format(ID, self.first, self.standard_after)
            page = scrapy.Request(url=url, callback=self.parse_page)
            # scrape posts
            for (shortcode, caption) in page:
                url = self.comments_url.format(shortcode, self.first, self.standard_after)
                comments = scrapy.Request(url=url, callback=self.parse_post)
                # save data as json
                with open("../../../data.json", "w", encoding="utf-8") as f:
                    json.dump({(shortcode, caption): comments})








    def parse_page(self, response):
        result = []
        # extract shortcodes
        for edge in response['data']['user']['edge_owner_to_timeline_media']['edges']:
            # (shortcode, caption)
            result.append((edge['node']['shortcode'], edge['node']['edge_media_to_caption']['edges']['0']['node']['text']))
        return result

    def parse_post(self, response):
        result = []
        # extract comments
        for edge in response['data']['shortcode_media']['edge_media_to_parent_comment']['edges']:
            # ((username, id), text)
            result.append(((edge['node']['owner']['username'], edge['node']['owner']['id']), edge['node']['text']))
        return result
