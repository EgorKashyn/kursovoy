import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class CAASSpider(CrawlSpider):
    name = 'CAAS'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    allowed_domains = ['www.agriculturejournals.cz']
    start_urls = ['https://www.agriculturejournals.cz']

    rules = (
        Rule(LinkExtractor(allow=('https://[a-z]+[.]agriculturejournals.cz')),
                            callback=None, follow=True),
    )

    def parse_item(self, response):
        item = {}
        filename = response.url.split('/')[-1]
        jrnl = filename.split('.')[0]
        if not 'CAAS' in os.listdir():
            os.mkdir('CAAS')
        if not jrnl in os.listdir('CAAS'):
            os.mkdir('CAAS\\' + jrnl)
        with open('CAAS\\' + jrnl + '\\' + filename + '.html', 'wb') as f:
            f.write(response.body)