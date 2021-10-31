import scrapy


class Instagram(scrapy.Spider):
    name = "instagram"


    def __init__(self, filepath, first=50, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        # Get Posts
        self.posts_url = """https://www.instagram.com/graphql/query/?query_hash=8c2a529969ee035a5063f2fc8602a0fd&variables={{"id":"{0}","first":{1},"after":"{2}"}}"""

        # Get Comments
        self.comments_url = """https://www.instagram.com/graphql/query/?query_hash=33ba35852cb50da46f5b5e889df7d159&variables={{"shortcode":"{0}","first":{1},"after":"{2}"}}"""

        # Number of Endpoints
        self.first = first

        self.standart_after = "{\"cached_comments_cursor\"%3A+\"17913168032100926\"%2C+\"bifilter_token\"%3A+\"KBgBCAAYABAACAAIAK9e469-P_-gSB8EEkAA\"}"


    def start_requests(self):
        with open(self.filepath, "r") as f:
            urls = f.readlines()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open("page.html", 'wb') as f:
            f.write(response.body)
