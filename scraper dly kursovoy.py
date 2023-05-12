import os
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class AeaSpider(CrawlSpider):
    name = 'AEA'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    allowed_domains = ['www.aeaweb.org']
    start_urls = ['https://www.aeaweb.org/journals']

    rules = (
        Rule(LinkExtractor(allow=('.+\/journals\/[aA-zZ]+'),
                           deny=(
                               '.*search.*', '.+\/journals\/[aA-zZ]+\/.+', '.+subscriptions.*',
                               '.*get-journal-alerts.*', '.*policies.*', '.*data.*', '.*jstor.*')),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('.+\/issues\/[0-9]+'),
                           deny=(
                               '.+\/issues\/[0-9]+[?].*', '.+search.+', '.+\/journals\/[aA-zZ]+\/.+',
                               '.+subscriptions.*', '.*isuues')),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('.+\/articles\?id=\d+\.\d+\/[a-z]+\..*')), callback=None, follow=False)
    )

    def parse_item(self, response):
        item = {}
        filename = response.url.split('/')[-1]
        jrnl = filename.split('.')[0]
        if not 'AEA' in os.listdir():
            os.mkdir('AEA')
        if not jrnl in os.listdir('AEA'):
            os.mkdir('AEA\\' + jrnl)
        with open('AEA\\' + jrnl + '\\' + filename + '.html', 'wb') as f:
            f.write(response.body)
        # item['issue_information'] = response.xpath('.//section[@class="issue-information"]/h2/text()').get()
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('.//section[@class="issue-information"]/h1/text()').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        yield item