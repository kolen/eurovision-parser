# Scrapy settings for eurov project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'eurov'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['eurov.spiders']
NEWSPIDER_MODULE = 'eurov.spiders'
DEFAULT_ITEM_CLASS = 'eurov.items.EurovItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

