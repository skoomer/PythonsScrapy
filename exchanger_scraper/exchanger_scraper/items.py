# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Exchanger(scrapy.Item):
    url = scrapy.Field()
    digital_code = scrapy.Field()
    alphabetic_code = scrapy.Field()
    number_of_currency_units = scrapy.Field()
    currency = scrapy.Field()
    official_rate = scrapy.Field()
