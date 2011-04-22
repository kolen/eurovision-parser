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
        Rule(SgmlLinkExtractor(allow=r'.*/page/history/by-year/contest\?event=\d+$'),
            callback='parse_page',
            follow=True),
    )

    def parse_page(self, response):
        hxs = HtmlXPathSelector(response)

        title = hxs.select('//div[@class="grid-column-block content-block is-not-tabbed cb-block cb-EventInfo cb-EventInfo-default"]/h2/text()')[0].extract()
        
        evtitle_m = re.match(r'^Eurovision Song Contest (\d{4})(.*)$', title)
        
        i = EurovItem()
        i['title'] = title
        i['year'] = evtitle_m.group(1)
        i['stage'] = evtitle_m.group(2)        
        
        participants = []
        p_rows = hxs.select("//table[@class='sortable participants no-arrow decorated']/tbody/tr")
        for p_row in p_rows:
            cols = p_row.select(".//td")
            country_number = int(cols[0].select("text()")[0].extract())
            country_name = cols[1].select(".//a/text()")[0].extract()
            country_broadcaster = cols[1].select(".//div/text()")[0].extract()
            country_performer = cols[2].select("text()").extract()[0].strip()
            country_song = cols[3].select("text()").extract()[0].strip()
            country_points = int(cols[4].select("text()").extract()[0])
            country_place = int(cols[5].select("text()").extract()[0])

            participants.append(
            {
                'number': country_number,
                'country': country_name,
                'broadcaster': country_broadcaster,
                'performer': country_performer,
                'song': country_song,
                'points': country_points,
                'place': country_place,
            })
        
        i['participants'] = participants

        score_strings = hxs.select("//*[contains(@class,'cb-EventInfo-scoreboard')]//tbody/tr/td/@title[contains(.,'goes to')]").extract()
        scores = []
        for score_string in score_strings:
            s = {}
            m = re.match("^(\d+)pt from (.+) goes to (.+)$", score_string)
            if m:
                s['country_from'] = m.group(2)
                s['country_to'] = m.group(3)
                s['score'] = int(m.group(1))
                
                scores.append(s)
                
        i['scores'] = scores
        
        
        details_rows = hxs.select('//table[@class="details"]/tr')
        details = dict(
            (row.select('th/text()').extract()[0].strip(),
            row.select('td/text()').extract()[0].strip())
            for row in details_rows)

        i['location'] = details.pop('Location', None)
        i['venue'] = details.pop('Venue', None)
        
        i['details'] = details

        return i
