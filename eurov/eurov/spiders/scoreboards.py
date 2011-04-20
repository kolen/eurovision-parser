import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from eurov.items import EurovItem

class ScoreboardsSpider(CrawlSpider):
    name = 'scoreboards'
    allowed_domains = ['eurovision.tv']
    start_urls = ['http://www.eurovision.tv/page/history/year']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'http://www.eurovision.tv/page/history/by-year/contest?event=\d+'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)

        title = hxs.select('//div[@class="grid-column-block content-block is-not-tabbed cb-block cb-EventInfo cb-EventInfo-default"]/h2/text()').extract()

        score_strings = hxs.select("//*[contains(@class,'cb-EventInfo-scoreboard')]//tbody/tr/td/@title[contains(.,'goes to')]").extract()
        for score_string in score_strings:
            m = re.match("^(\d+)pt from (.+) goes to (.+)$", score_string)
            if m:
                 i = EurovItem()
                 i['title'] = title 
                 i['country_from'] = m.group(2)
                 i['country_to'] = m.group(3)
                 i['score'] = m.group(1)
                 yield i
