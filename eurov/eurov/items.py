# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class EurovItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    country_from = Field()
    country_to = Field()
    score = Field()

    event_country = Field()
    event_host_broadcaster = Field()
    event_venue = Field()
    event_hosts = Field()
    event_num_participants = Field()
    event_voting_method = Field()
    event_interval_act = Field()

    country_from_number = Field()
    country_from_name = Field()
    country_from_broadcaster = Field()
    country_from_performer = Field()
    country_from_song = Field()
    country_from_points = Field()
    country_from_place = Field()
