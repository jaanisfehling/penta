import scrapy


class Instagram(scrapy.Spider):
    name = "instagram"
    base_url = """https://www.instagram.com/graphql/query/?query_hash={0}&variables={{"shortcode":"{1}","first":50,"after":"{2}"}}"""
    # Comments
    query_hash = "33ba35852cb50da46f5b5e889df7d159"
    query_comments_vars = '{{"shortcode":"{0}","first":50,"after":"{1}"}}'
    # Post
    shortcode = ""

    urls = []


    def start_requests(self):
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open("page.html", 'wb') as f:
            f.write(response.body)
