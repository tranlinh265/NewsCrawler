# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VbplNewsCrawlerItem(scrapy.Item):
  doc_id = scrapy.Field()
  title = scrapy.Field()
  url = scrapy.Field()
  description = scrapy.Field()
  content = scrapy.Field()
  public_date = scrapy.Field()
  created_at = scrapy.Field()
  updated_at = scrapy.Field()
