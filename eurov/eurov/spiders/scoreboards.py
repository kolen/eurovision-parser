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
        
        props = hxs.select("//table[@class='details']//td/text()").extract()

        participants_data = {}

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

            participants_data[country_name] = {
                'number': country_number,
                'name': country_name,
                'broadcaster': country_broadcaster,
                'performer': country_performer,
                'song': country_song,
                'points': country_points,
                'place': country_place,
            }

        score_strings = hxs.select("//*[contains(@class,'cb-EventInfo-scoreboard')]//tbody/tr/td/@title[contains(.,'goes to')]").extract()
        for score_string in score_strings:
            m = re.match("^(\d+)pt from (.+) goes to (.+)$", score_string)
            if m:
                i = EurovItem()
                
                evtitle_m = re.match(r'^Eurovision Song Contest (\d{4})(.*)$', title)
                
                i['event_title'] = title
                i['year'] = evtitle_m.group(1)
                i['stage'] = evtitle_m.group(2)
                
                i['country_from'] = m.group(2)
                i['country_to'] = m.group(3)
                i['score'] = m.group(1)
                
                i['event_country'] = props[0]
                i['event_host_broadcaster'] = props[1]
                i['event_venue'] = props[2]
                i['event_hosts'] = props[3]
                i['event_num_participants'] = props[4]
                i['event_voting_method'] = props[5]
                #i['event_interval_act'] = props[6]

                country_data = participants_data.get(i['country_from'])
                if country_data:
                    i['country_from_number'] = country_data['number']
                    i['country_from_name'] = country_data['name']
                    i['country_from_broadcaster'] = country_data['broadcaster']
                    i['country_from_performer'] = country_data['performer']
                    i['country_from_song'] = country_data['song']
                    i['country_from_points'] = country_data['points']
                    i['country_from_place'] = country_data['place']                

                yield i
