from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from myproject.items import MyprojectItem
import re
from parsel import Selector
class OCPSpider(CrawlSpider):

    name = 'OCP'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'FILES_STORE': "data/"+name
    }

    allowed_domains = ['www.oldcitypublishing.com']

    start_urls = ['https://www.oldcitypublishing.com/journals/']

    rules = (
        Rule(LinkExtractor(allow=('journals/[a-z]+-home/$')),
                            callback=None, follow=True),
        Rule(LinkExtractor(allow=('journals/[a-z]+-home/[a-z]+-issue-contents/$')),
             callback=None, follow=True),
        Rule(LinkExtractor(allow=('journals/[a-z]+-home/[a-z]+-issue-contents/[a-z]+-volume-\d+-number-\d+-\d+-\d+/$')),
             callback='parse_item', follow=False)
    )

    def parse_item(self, response):
        urls = []
        s = response.xpath('//a[contains(text(),"abstract") or contains(text(),"Abstract")]')
        if s:
            for i in s:
                urls.append(response.urljoin(i.attrib['href']))
        else:
            return
        item = MyprojectItem()
        item['file_urls'] = urls
        yield item